import json
from django.db.models import Prefetch, Sum, Min
from django import forms
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from quran.models import Page, Aya, Word, DistinctWord, Translation
from quran.views import prefetch_aya_translations, get_setting
from quranfal.models import UserAya, UserWord, List
from django.http import HttpResponseRedirect


class LearningPageView(TemplateView):
    template_name = 'quranfal/page.html'

    def get_context_data(self, page_number, **kwargs):
        context = super(LearningPageView, self).get_context_data(**kwargs)

        page = Page.objects.get(number=page_number)

        context['learning'] = False
        user_words = []
        context['not_logged_in'] = True
        if self.request.user.is_authenticated():
            context['learning'] = get_setting(self.request, 'learning')
            context['not_logged_in'] = False
            user = self.request.user
            # user_aya_qs = UserAya.objects.filter(user=user).select_related('list')
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id) \
                .prefetch_related(prefetch_aya_translations(self.request))  # filtering on membership table so prefetch membership table!
                    # later: , Prefetch('user_ayas', queryset=user_aya_qs)

            known_distinct_words = DistinctWord.objects.filter(user_words__user=user)
            user_words = Word.objects.filter(
                aya_id__gte=page.aya_begin_id,
                aya_id__lte=page.aya_end_id,
                distinct_word__in=known_distinct_words)\
                .values_list('aya__sura_id', 'aya__number', 'number', 'distinct_word__user_words__list_id')
            user_words = [list(word) for word in user_words]
        else:
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id) \
                .prefetch_related(prefetch_aya_translations(self.request))

        context['ayas'] = ayas
        context['show_word_meanings'] = get_setting(self.request, 'show_word_meanings')
        context['user_words'] = json.dumps(user_words)
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
        return HttpResponse('User is created.<script>closeFancyBox(1000);location.reload();toastr.info("Are you the 6 fingered man?");</script>',
                            content_type='text/html')

TOTAL_WORD_COUNT=77429

class LearningMarkWord(View):
    def get_list_stats (self, list_id):
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
        deleted=False
        if user_word:
            old_stats = self.get_list_stats(user_word.list_id)
            old_stats['distinct_word_count'] -= 1
            old_stats['word_count'] -= word.distinct_word.count

            if user_word.list_id != int(list_id):
                user_word.list_id = list_id # update
            else:
                user_word.delete()
                deleted=True
        else:
            user_word = UserWord(user=request.user, distinct_word=word.distinct_word, list_id=list_id)

        if deleted: # not deleted
            msg = 'Word %s is deleted.\n There are %d words in the %s (%.2f%% of the Quran).' % (word.utext, old_stats['distinct_word_count'], list_name, old_stats['word_count']/TOTAL_WORD_COUNT*100)
        else:
            new_stats = self.get_list_stats(list_id)
            new_stats['distinct_word_count'] += 1
            new_stats['word_count'] += word.distinct_word.count

            user_word.save()


            msg = 'Word %s is %d times in Quran!\nThere are %d words in the %s (%.2f%% of the Quran).' % \
                  (word.utext, word.distinct_word.count, new_stats['distinct_word_count'], list_name, new_stats['word_count']/TOTAL_WORD_COUNT*100)

        message = {
            'message': msg,
            'list': 0 if deleted else user_word.list_id
        }
        return HttpResponse(json.dumps(message), content_type='text/html')


class SettingsForm(forms.Form):
    translation = forms.ChoiceField(choices=[(t.id, t.text) for t in Translation.objects.all()])
    learning = forms.BooleanField(required=False)
    show_word_meanings = forms.BooleanField(required=False)


def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            request.session['translation'] = form.cleaned_data['translation']
            request.session['learning'] = form.cleaned_data['learning']
            request.session['show_word_meanings'] = form.cleaned_data['show_word_meanings']
            return HttpResponseRedirect('/quran/page/6/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SettingsForm(initial={
            'translation':get_setting(request, 'translation'),
            'learning':get_setting(request, 'learning'),
            'show_word_meanings': get_setting(request, 'show_word_meanings'),
        })

    return render(request, 'quranfal/settings.html', {'form': form})


def saved(request):
    uw = UserWord.objects.filter(user=request.user, list_id=2)
    dw_id = uw.values_list('distinct_word_id', flat=True)
    dw = DistinctWord.objects.filter(id__in=dw_id)
    w_first_id = dw.annotate(first_word=Min('words')).values_list('first_word', flat=True)
    w = Word.objects.filter(id__in=w_first_id)

    return render(request, 'quranfal/study.html', {'words': w})

def frequent(request):
    pass