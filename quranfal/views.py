import json

from django.db.models import Prefetch, Sum, Min
from django import forms
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView, View
from quran.models import *
from quranfal.models import *


class UserView:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_words = []

    def add_to_user_words(self, ayas):
        known_distinct_words = DistinctWord.objects.filter(user_words__user=self.request.user)
        extra_words = Word.objects.filter(
            aya__in=ayas,
            distinct_word__in=known_distinct_words) \
            .values_list('aya__sura_id', 'aya__number', 'number', 'distinct_word__user_words__list_id')
        self.user_words = self.user_words + [list(word) for word in extra_words]

    def get_user_words_as_json(self):
        return json.dumps(self.user_words)

    def get_user_context(self):
        extra_context = {}
        extra_context['show_word_meanings'] = get_setting(self.request, 'show_word_meanings')
        extra_context['show_translation'] = get_setting(self.request, 'show_translation')
        extra_context['can_mark_known_words'] = False
        extra_context['can_mark_unknown_words'] = False
        extra_context['not_logged_in'] = True
        if self.request.user.is_authenticated():
            extra_context['can_mark_known_words'] = get_setting(self.request, 'can_mark_known_words')
            extra_context['can_mark_unknown_words'] = get_setting(self.request, 'can_mark_unknown_words')
            extra_context['not_logged_in'] = False
        return extra_context


class PageView(TemplateView, UserView):
    template_name = 'quranfal/page.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        UserView.__init__(self)
        self.page_number = 0

    # sets cookie on response
    def render_to_response(self, context, **response_kwargs):
        response = super(PageView, self).render_to_response(context, **response_kwargs)
        response.set_cookie("page_number", self.page_number)
        return response

    def get_context_data(self, page_number, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        user_context = super(PageView, self).get_user_context()
        context = dict(list(context.items()) + list(user_context.items()))
        # context = {**context, **user_context} # in python 3.5

        if int(page_number) == 0:
            page_number = get_setting(self.request, 'page_number')

        self.page_number = page_number # to set cookie on response

        page = Page.objects.get(number=page_number)

        if self.request.user.is_authenticated():
            # user_aya_qs = UserAya.objects.filter(user=user).select_related('list')
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id) \
                .prefetch_related(
                prefetch_aya_translations(self.request), 'word_meanings')  # filtering on membership table so prefetch membership table!
            # later: , Prefetch('user_ayas', queryset=user_aya_qs)

            if context['can_mark_known_words'] or context['can_mark_unknown_words']:
                self.add_to_user_words(ayas)
        else:
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id) \
                .prefetch_related(prefetch_aya_translations(self.request), 'word_meanings')

        add_word_meanings_json(ayas)

        context['ayas'] = ayas
        context['user_words'] = self.get_user_words_as_json()
        context['page_number'] = int(page_number)
        return context





class LearningMarkAya(View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        sura_number = request.POST.get('sura')
        aya_number = request.POST.get('aya')
        aya = Aya.objects.filter(sura_id=sura_number, number=aya_number).first()
        user_aya = aya.user_ayas.filter(user=user).first()
        user_aya.list_id += 1
        return HttpResponse(
            'User is created.<script>closeFancyBox(1000);location.reload();toastr.info("Are you the 6 fingered man?");</script>',
            content_type='text/html')


TOTAL_WORD_COUNT = 77429


class LearningMarkWord(View):
    def get_list_stats(self, list_id):
        if 'stats' not in self.request.session:
            self.request.session['stats'] = {}
        stats = self.request.session['stats']
        index = str(list_id)
        if index not in stats:
            stats[index] = {
                'distinct_word_count': UserWord.objects
                    .filter(user=self.request.user, list_id=list_id)
                    .count(),
                'word_count': UserWord.objects
                    .filter(user=self.request.user, list_id=list_id)
                    .aggregate(sum=Coalesce(Sum('distinct_word__count'), 0))['sum'],
            }
        return stats[index]

    def post(self, request, *args, **kwargs):

        list_id = request.POST.get('list')

        if request.POST.get('word_id', None):
            word_id = request.POST.get('word_id')
            word = Word.objects.get(id=word_id)
        else:
            sura_number = request.POST.get('sura')
            aya_number = request.POST.get('aya')
            word_number = request.POST.get('word')
            word = Word.objects.filter(sura_id=sura_number, aya__number=aya_number, number=word_number).first()

        list_name = List.objects.get(id=list_id).name.lower()
        user_word = word.distinct_word.user_words.filter(user=self.request.user).first()
        deleted = False
        if user_word:
            old_stats = self.get_list_stats(user_word.list_id)
            old_stats['distinct_word_count'] -= 1
            old_stats['word_count'] -= word.distinct_word.count

            if user_word.list_id != int(list_id):
                user_word.list_id = list_id  # update
            else:
                user_word.delete()
                deleted = True
        else:
            user_word = UserWord(user=request.user, distinct_word=word.distinct_word, list_id=list_id)

        if deleted:  # not deleted
            msg = 'Word %s is deleted.\n There are %d words in the %s (%.2f%% of the Quran).' % (
            word.utext, old_stats['distinct_word_count'], list_name, old_stats['word_count'] / TOTAL_WORD_COUNT * 100)
        else:
            new_stats = self.get_list_stats(list_id)
            new_stats['distinct_word_count'] += 1
            new_stats['word_count'] += word.distinct_word.count

            user_word.save()

            msg = 'Word %s is %d times in Quran!\nThere are %d words in the %s (%.2f%% of the Quran).' % \
                  (word.utext, word.distinct_word.count, new_stats['distinct_word_count'], list_name,
                   new_stats['word_count'] / TOTAL_WORD_COUNT * 100)

        message = {
            'message': msg,
            'list': 0 if deleted else user_word.list_id
        }
        return HttpResponse(json.dumps(message), content_type='text/html')


class SettingsForm(forms.Form):
    translation_type = forms.ChoiceField(choices=[(t.id, t.text) for t in Translation.objects.all()])
    show_translation = forms.BooleanField(required=False)
    show_word_meanings = forms.BooleanField(required=False)
    can_mark_known_words = forms.BooleanField(required=False)
    can_mark_unknown_words = forms.BooleanField(required=False)


def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            response = HttpResponse('<script>location.reload();</script>', content_type='text/html')
            response.set_cookie('translation_type', form.cleaned_data['translation_type'])
            response.set_cookie('show_translation', form.cleaned_data['show_translation'])
            response.set_cookie('show_word_meanings', form.cleaned_data['show_word_meanings'])
            response.set_cookie('can_mark_known_words', form.cleaned_data['can_mark_known_words'])
            response.set_cookie('can_mark_unknown_words', form.cleaned_data['can_mark_unknown_words'])
            return response

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SettingsForm(initial={
            'translation_type': get_setting(request, 'translation_type'),
            'show_translation': get_setting(request, 'show_translation'),
            'show_word_meanings': get_setting(request, 'show_word_meanings'),
            'can_mark_known_words': get_setting(request, 'can_mark_known_words'),
            'can_mark_unknown_words': get_setting(request, 'can_mark_unknown_words'),
        })

        not_logged_in = True
        if request.user.is_authenticated():
            not_logged_in = False

    return render(request, 'quranfal/settings.html', {'form': form, 'not_logged_in': not_logged_in})


def saved(request):
    uw = UserWord.objects.filter(user=request.user, list_id=2)
    dw_id = uw.values_list('distinct_word_id', flat=True)
    dw = DistinctWord.objects.filter(id__in=dw_id)
    w_first_id = dw.annotate(first_word=Min('words')).values_list('first_word', flat=True)
    w = Word.objects.filter(id__in=w_first_id)

    return render(request, 'quranfal/study.html', {'words': w})


def frequent(request):
    pass

# default settings
default_settings = {
    'translation_type': 2, #Translation.objects.first().id, # problem for migrating to another server
    'show_translation': True,
    'show_word_meanings': True,
    'can_mark_known_words': True,
    'can_mark_unknown_words': True,
    'page_number': 1,
}

def get_setting(request, setting):
    if setting in request.COOKIES:
        if request.COOKIES[setting] == 'False':
            return False
        if request.COOKIES[setting] == 'None':
            return None
        return request.COOKIES[setting]
    return default_settings[setting]

def prefetch_aya_translations(request):
    translation_id = get_setting(request, 'translation_type')
    return Prefetch('translations', queryset=AyaTranslation.objects.filter(translation_id=translation_id))


class AyaView(TemplateView, UserView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        UserView.__init__(self)

    template_name='quranfal/aya.html'
    def get_context_data(self, sura_number, aya_number, **kwargs):
        context = super(AyaView, self).get_context_data(**kwargs)
        user_context = super(AyaView, self).get_user_context()
        context = dict(list(context.items()) + list(user_context.items()))

        aya = Aya.objects.filter(sura__number=sura_number, number=aya_number)\
            .prefetch_related(prefetch_aya_translations(self.request), 'word_meanings')

        add_word_meanings_json(aya)

        if context['can_mark_known_words'] or context['can_mark_unknown_words']:
            self.add_to_user_words(aya)

        context['user_words'] = self.get_user_words_as_json()
        context['aya'] = aya[0]

        return context


# make sure to add .prefetch_related('word_meanings') beforehand
def add_word_meanings_json(aya):
    for aya_ in aya:
        meanings = sorted(aya_.word_meanings.all(), key=lambda x: x.number)
        meanings = [meaning.ttext for meaning in meanings]
        aya_.word_meanings_json = '["' + '", "'.join(meanings) + '"]'


class WordView(TemplateView, UserView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        UserView.__init__(self)

    template_name='quranfal/word.html'
    def get_context_data(self, sura_number, aya_number, word_number, **kwargs):
        context = super(WordView, self).get_context_data(**kwargs)
        user_context = super(WordView, self).get_user_context()
        context = dict(list(context.items()) + list(user_context.items()))

        aya = Aya.objects.filter(sura__number=sura_number, number=aya_number) \
            .prefetch_related(prefetch_aya_translations(self.request), 'word_meanings')

        add_word_meanings_json (aya)
        aya = aya[0]

        word = Word.objects.filter(aya=aya, number=word_number).prefetch_related()  # todo cant see extent of data brought
        the_word = word[0] # one less trip to db

        # other ayas with same word
        ayas = Aya.objects.filter(words__distinct_word=the_word.distinct_word) \
            .order_by('sura_id', 'number') \
            .prefetch_related(prefetch_aya_translations(self.request), 'word_meanings')
        # prefetch does not like flat values so cant put values_list here

        add_word_meanings_json (ayas)

        # pull user words from the db
        if context['can_mark_known_words'] or context['can_mark_unknown_words']:
            self.add_to_user_words([aya_.id for aya_ in ayas] + [aya.id]) # one less trip to the db by combining the two

        context['word'] = the_word
        context['aya'] = aya
        context['ayas'] = ayas

        return context


class LemmaView(TemplateView, UserView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        UserView.__init__(self)

    template_name='quranfal/lemma.html'
    def get_context_data(self, lemma_id, **kwargs):
        context = super(LemmaView, self).get_context_data(**kwargs)
        user_context = super(LemmaView, self).get_user_context()
        context = dict(list(context.items()) + list(user_context.items()))

        lemma = get_object_or_404(Lemma, pk=lemma_id)
        aya_translation_queryset = AyaTranslation.objects.filter(translation_id=get_setting(self.request, 'translation_type'))
        words = lemma.words.all() \
            .order_by('sura_id', 'aya_id') \
            .prefetch_related(Prefetch('aya__translations', queryset=aya_translation_queryset)) \
            .prefetch_related('aya__word_meanings')

        if context['can_mark_known_words'] or context['can_mark_unknown_words']:
            ayas = [word.aya for word in words]
            self.add_to_user_words(ayas)
        context['user_words'] = self.get_user_words_as_json()

        add_word_meanings_json(ayas)

        context['lemma'] = lemma
        context['words'] = words

        return context


class RootView(TemplateView, UserView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        UserView.__init__(self)

    template_name='quranfal/root.html'
    def get_context_data(self, root_id, **kwargs):
        context = super(RootView, self).get_context_data(**kwargs)
        user_context = super(RootView, self).get_user_context()
        context = dict(list(context.items()) + list(user_context.items()))

        # .prefetch_related('words__aya') \
        lemmas = Lemma.objects.filter(root__id=root_id)\
            .prefetch_related(Prefetch('words__aya__translations', queryset=AyaTranslation.objects.filter(translation_id=get_setting(self.request, 'translation_type')))) \
            .prefetch_related('words__aya__word_meanings')
        context['lemmas'] = lemmas  # , 'ayas': ayas

        ayas=[]
        for lemma in lemmas:
            for word in lemma.words.all():
               ayas = ayas + [word.aya]

        if context['can_mark_known_words'] or context['can_mark_unknown_words']:
            self.add_to_user_words(ayas)
            context['user_words'] = self.get_user_words_as_json()

        add_word_meanings_json(ayas)
        return context



class IndexView(TemplateView):
    template_name = 'quranfal/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        suras = get_list_or_404(Sura)
        context['suras'] = suras

        return context


class SuraView(TemplateView):
    template_name = 'quranfal/sura.html'
    def get_context_data(self, sura_number, **kwargs):
        context = super(SuraView, self).get_context_data(**kwargs)
        ayas = Aya.objects.filter(sura__number=sura_number)\
            .prefetch_related(prefetch_aya_translations(self.request))
        context['ayas'] = ayas

        return context


class RootIndexView(TemplateView):
    template_name = 'quranfal/root_index.html'
    def get_context_data(self, **kwargs):
        context = super(RootIndexView, self).get_context_data(**kwargs)
        roots = Root.objects.all().order_by('utext')
        context['roots'] = roots

        return context