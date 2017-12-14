import os
import sys

# ~~~~~~~~~~~~ Directory Paths ~~~~~~~~~~~~~~~

BASE_DIRECTORY = os.path.dirname(os.path.dirname(__file__))  # src/ directory

sys.path.insert(1, os.path.join(BASE_DIRECTORY, 'apps'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SECRET_FILE = os.path.normpath(os.path.join(BASE_DIRECTORY, 'SECRET.key'))

ADMINS = (
    ('Zeeshan Asgar', 'asgarzeeshan@gmail.com'),
)

MANAGERS = ADMINS

SESSION_COOKIE_AGE = 31536000

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_swagger',
    'accounts.apps.AccountConfig',

]

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += DEFAULT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'src.urls'

WSGI_APPLICATION = 'src.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_PATH = os.path.join(BASE_DIRECTORY, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIRECTORY, 'media')
MEDIA_URL = '/media/'
PDF_ROOT = os.path.join(STATIC_PATH, 'pdf')

STATIC_ROOT = os.path.join(BASE_DIRECTORY, "..", "static")
STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_PATH = os.path.join(BASE_DIRECTORY, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S%z",
    'DATE_FORMAT': "%Y-%m-%d",
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning'
}

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string

        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Unable to open %s' % SECRET_FILE)

from .env import *
