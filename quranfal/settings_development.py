# coding=utf-8
from .settings_common import *

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'edgleweb',
        'PASSWORD': 'edgleweb',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'options': '-c search_path=quran'
        }
    }

INSTALLED_APPS += [
    # 'debug_toolbar',
]

INTERNAL_IPS = ('10.0.2.2','10.0.2.15')  # needed for debug_toolbar / vagrant ip




