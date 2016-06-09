import json
from django.db.models import Prefetch
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from quran.models import Page, Aya, Word, DistinctWord
from quran.views import prefetch_aya_translations, get_setting
from quranfal.models import UserAya, UserWord, List


class LearningPageView(TemplateView):
    template_name='quran/page.html'
    def get_context_data(self, page_number, **kwargs):
        context = super(LearningPageView, self).get_context_data(**kwargs)

        page = Page.objects.get(number=page_number)

        context['learning'] = False
        user_words = []
        if self.request.user.is_authenticated():
            context['learning'] = self.request.session['learning']
            user = self.request.user
            list_qs = UserAya.objects.filter(user=user).select_related('list')
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id)\
                .prefetch_related(prefetch_aya_translations(self.request),
                                  Prefetch('userayas', queryset=list_qs)) # filtering on membership table so prefetch membership table!

            known_distinct_words=DistinctWord.objects.filter(userwords__user=user)
            user_words = Word.objects.filter(
                aya_id__gte=page.aya_begin_id,
                aya_id__lte=page.aya_end_id,
                distinct_word__in=known_distinct_words).values_list('aya__sura_id', 'aya__number', 'number', 'distinct_word__userwords__list_id')
            user_words = [list(word) for word in user_words]
        else:
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id)\
                .prefetch_related(prefetch_aya_translations(self.request))

        context['ayas'] = ayas
        context['display_word_meanings'] = get_setting(self.request, 'display_word_meanings')
        context['user_words'] = json.dumps(user_words)
        return context


class LearningMarkAya(View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        sura_number = request.POST.get('sura')
        aya_number = request.POST.get('aya')
        aya=Aya.objects.filter(sura_id=sura_number, number=aya_number).first()
        user_aya=aya.userayas.filter(user=user).first()
        user_aya.list_id += 1
        return HttpResponse('User is created.<script>closeFancyBox(1000);location.reload();toastr.info("Are you the 6 fingered man?");</script>',
                                content_type='text/html')


class LearningMarkWord(View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        sura_number = request.POST.get('sura')
        aya_number = request.POST.get('aya')
        word_number = request.POST.get('word')
        word = Word.objects.filter(sura_id=sura_number, aya__number=aya_number, number=word_number).first()
        user_word = word.distinct_word.userwords.filter(user=user).first()
        if user_word:
            new_list = List.objects.filter(id=user_word.list_id+1).first()
            if not new_list:
                new_list = List.objects.first()
            user_word.list = new_list
        else:
            user_word = UserWord(user=user, distinct_word=word.distinct_word, list=List.objects.first())
        user_word.save()

        message = {
            'message': 'Word is added!',
            'list': user_word.list_id,
            'script': 'rr',
        }
        return HttpResponse(json.dumps(message), content_type='text/html')

