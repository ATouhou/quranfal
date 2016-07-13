"""quranfalweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView

from quranfal.views import *


urlpatterns = [

    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^quran/page/(?P<page_number>\d+)/$', PageView.as_view(), name='quran_page'),
    url(r'^quran/learning/aya/$', login_required(LearningMarkAya.as_view()), name='learning_mark_aya'),
    url(r'^quran/learning/word/$', login_required(LearningMarkWord.as_view()), name='learning_mark_word'),

    url(r'^quran/settings/$', settings, name='learning_mark_word'),

    url(r'^quran/study/saved/$', login_required(saved), name='learning_mark_word'),
    url(r'^quran/study/frequent/$', login_required(frequent), name='learning_mark_word'),

    url(r'^quran/$', IndexView.as_view(), name='quran_index'),
    url(r'^quran/(?P<sura_number>\d+)/$', SuraView.as_view(), name='quran_sura'),
    url(r'^quran/(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', AyaView.as_view(), name='quran_aya'),
    url(r'^quran/(?P<sura_number>\d+)/(?P<aya_number>\d+)/(?P<word_number>\d+)/$', WordView.as_view(), name='quran_word'),

    url(r'^quran/lemma/(?P<lemma_id>\d+)/$', LemmaView.as_view(), name='quran_lemma'),
    url(r'^quran/root/(?P<root_id>\d+)/$', RootView.as_view(), name='quran_root'),
    url(r'^quran/root/$', RootIndexView.as_view(), name='quran_root_index'),


    url(r'^', RedirectView.as_view(url='/quran/page/0/')),
]
