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

from quranfal.views import LearningPageView, LearningMarkAya, LearningMarkWord, settings

urlpatterns = [

    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^quran/page/(?P<page_number>\d+)/$', LearningPageView.as_view(), name='quran_page'),
    url(r'^quran/learning/aya/$', login_required(LearningMarkAya.as_view()), name='learning_mark_aya'),
    url(r'^quran/learning/word/$', login_required(LearningMarkWord.as_view()), name='learning_mark_word'),

    url(r'^quran/settings/$', login_required(settings), name='learning_mark_word'),

    url(r'^quran/', include('quran.urls')),

    url(r'^', RedirectView.as_view(url='/quran/page/1/')),
]
