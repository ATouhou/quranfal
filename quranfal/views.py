from django.db.models import Prefetch
from django.http import HttpResponse
from django.views.generic import TemplateView
from quran.models import Page, Aya, Word, DistinctWord
from quran.views import prefetch_aya_translations

from quranfal.models import UserAya, UserWord


class LearningPageView(TemplateView):
    template_name='quran/page.html'
    def get_context_data(self, page_number, **kwargs):
        context = super(LearningPageView, self).get_context_data(**kwargs)

        page = Page.objects.get(number=page_number)

        context['learning'] = False
        known_words = []
        if self.request.user.is_authenticated():
            context['learning'] = self.request.session['learning']
            user = self.request.user
            list_qs = UserAya.objects.filter(user=user).select_related('list')
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id)\
                .prefetch_related(prefetch_aya_translations(self.request),
                                  Prefetch('userayas', queryset=list_qs)) # filtering on membership table so prefetch membership table!

            known_distinct_words=DistinctWord.objects.filter(userwords__user=user)
            known_words = Word.objects.filter(
                aya_id__gte=page.aya_begin_id,
                aya_id__lte=page.aya_end_id,
                distinct_word__in=known_distinct_words).values_list('utext', flat=True)
        else:
            ayas = Aya.objects.filter(id__gte=page.aya_begin_id, id__lte=page.aya_end_id)\
                .prefetch_related(prefetch_aya_translations(self.request))

        context['ayas'] = ayas
        context['display_word_meaning'] = self.request.session['display_word_meaning']
        context['known_words'] = '[' + '", "'.join(known_words) + ']'
        return context


class LearningMarkAya(TemplateView):
    def get_context_data(self, sura_number, aya_number, **kwargs):
        context = super(LearningMarkAya, self).get_context_data(**kwargs)
        user = self.request.user
        aya=Aya.objects.filter(sura_id=sura_number, number=aya_number).first()
        user_aya=aya.userayas.filter(user=user).first()
        user_aya.list_id += 1
        return HttpResponse('User is created.<script>closeFancyBox(1000);location.reload();toastr.info("Are you the 6 fingered man?");</script>',
                                content_type='text/html')


class LearningMarkWord(TemplateView):
    def get_context_data(self, sura_number, aya_number, word_number, **kwargs):
        context = super(LearningMarkWord, self).get_context_data(**kwargs)
        user = self.request.user
        word = Word.objects.filter(sura_id=sura_number, aya_number=aya_number, number=word_number).first()
        user_word = word.userwords.filter(user=user).first()
        user_word.list_id += 1
        return HttpResponse('User is created.<script>closeFancyBox(1000);location.reload();toastr.info("Are you the 6 fingered man?");</script>',
                                content_type='text/html')

