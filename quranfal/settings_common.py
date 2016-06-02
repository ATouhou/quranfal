from .settings_default import *

INSTALLED_APPS += [
    'django.contrib.admindocs',
    'django.contrib.sites',  # needed for allauth

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'bootstrap3',
]

MIDDLEWARE_CLASSES += []

TEMPLATES[0]['DIRS'] = ['templates']
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.template.context_processors.request',  # needed for allauth
]

# extra locations for collectstatic command & staticfiles app will check other than app/static/app folders
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# # the absolute path to the directory where collectstatic will collect static files for deployment
# STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

# don't need these
USE_I18N = False # translation
USE_L10N = False # local format for numbers, date etc
USE_TZ = False # time zone aware times

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }


"""
NOTES:

# STATIC_URL default /static/, # base url to use when referring to static files in STATIC_ROOT. Example: "/static/" or "http://static.example.com/"
# MEDIA_ROOT # absolute filesystem path to the directory that will hold user-uploaded files.
# MEDIA_URL # URL for the media in MEDIA_ROOT
"""


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # Needed to login by username in Django admin, regardless of `allauth` ??
    'allauth.account.auth_backends.AuthenticationBackend', # `allauth` specific authentication methods, such as login by e-mail
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # prints emails to console # needed for allauth


# APP SPECIFIC SETTINGS #############################################################################################################################
# allauth ###########################################################################################################################################
SITE_ID = 1
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True # works if email confirmation done in the same browser as signing up
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Quran] "
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
# ACCOUNT_SIGNUP_FORM_CLASS = "school.forms.SignupForm"

LOGIN_URL = '/accounts/login/'  # needed for allauth
LOGIN_REDIRECT_URL = '/quran/'  # needed for allauth

# Bootstrap3 ########################################################################################################################################
BOOTSTRAP3 = {
    # The URL to the jQuery JavaScript file
    'jquery_url': '//code.jquery.com/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/',

    # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
    'css_url': None,

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': None,

    # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': False,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-3',

    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',

    # Set HTML required attribute on required fields
    'set_required': True,

    # Set HTML disabled attribute on disabled fields
    'set_disabled': False,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'has-error',

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': 'has-success',

    # Renderers (only set these if you have studied the source and understand the inner workings)
    'formset_renderers': {
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}

#####################################################################################################################################################
