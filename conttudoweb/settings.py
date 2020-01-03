"""
Django settings for conttudoweb project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from decouple import config, Csv
from dj_database_url import parse as dburl

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

DEVELOPER = config('DEVELOPER', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']

ADMINS = [('Alessandro', 'alessandrolimafolk@gmail.com'), ]

AUTH_USER_MODEL = 'authentication.MyUser'

# Email configuration

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='admin@admin.com')
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Application definition

# customizations
ADMIN_SITE_TITLE = config('ADMIN_SITE_TITLE', default='ConTTudOweb')
ADMIN_SITE_HEADER = config('ADMIN_SITE_HEADER', default='ConTTudO soluções web')
ADMIN_INDEX_TITLE = config('ADMIN_INDEX_TITLE', default='Controles do ConTTudOweb App')

PUBLIC_SCHEMA_NAME = 'public'

TENANT_MODEL = "tenants.Client"

SHARED_APPS = ["tenant_schemas", "conttudoweb.tenants"]

TENANT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "test_without_migrations",
    "django_extensions",
    "debug_toolbar",

    "conttudoweb.authentication",
    "conttudoweb.core",
    "conttudoweb.accounting",
]

if DEVELOPER:
    TENANT_APPS += [
        'django.contrib.admindocs',
    ]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    # 'tenant_schemas.middleware.DefaultTenantMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'conttudoweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'conttudoweb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
default_dburl = 'postgres://postgres:postgres@127.0.0.1:5432/ConTTudOwebApp'
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}
DATABASES['default']['ENGINE'] = 'tenant_schemas.postgresql_backend'
DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = config('DATA_UPLOAD_MAX_NUMBER_FIELDS', default=1000, cast=int)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'
