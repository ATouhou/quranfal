# coding=utf-8

from .settings_common import *

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'quran4.me', 'www.quran4.me']


DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'quranfalweb',
    'USER': 'quranfalweb',
    'PASSWORD': 'quranfalweb',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    'ATOMIC_REQUESTS': True,
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

del EMAIL_BACKEND # to go back to default