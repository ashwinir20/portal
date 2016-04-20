"""
Django settings for cloudmesh_portal project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

SITE_ID = 1

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# Include BOOTSTRAP3_FOLDER in path
BOOTSTRAP3_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'bootstrap3'))
if BOOTSTRAP3_FOLDER not in sys.path:
    sys.path.insert(0, BOOTSTRAP3_FOLDER)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gw=857%2gacc+b08kvygbsmvt+#(o51nw@40t2uk3xei2@qzzk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'cloudmesh_portal.users',
    'django_countries',
    'django_yubico',
    'rest_framework',
    'rest_framework_swagger',
    'bootstrap3'
)

# INSTALLED_APPS += ('bootstrap3',)
# INSTALLED_APPS += ('bootstrap_themes',)
INSTALLED_APPS += ('django_jinja',)
# INSTALLED_APPS += ('bootstrapform_jinja',)
INSTALLED_APPS += ('django_jinja.contrib._humanize',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'cloudmesh_portal.urls'

# os.path.join(BASE_DIR, 'templates'),

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        'DIRS': [os.path.join(BASE_DIR, 'cloudmesh_portal', 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'cloudmesh_portal', 'templates')],
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

WSGI_APPLICATION = 'cloudmesh_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# noinspection PyRedeclaration
ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/static/',
)

STATIC_URL = os.path.join(BASE_DIR, "static/")
STATIC = '/static/'
LOGIN_URL = '/user/login'
LOGIN_REDIRECT_URL = '/dashboard/'

cm_theme = 'cosmo'

# Default settings
BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': '//code.jquery.com/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/',

    # The complete URL to the Bootstrap CSS file (None means derive it
    # from base_url)
    # 'css_url': None,
    'css_url': 'https://maxcdn.bootstrapcdn.com/bootswatch/3.3.5/' +
               cm_theme + '/bootstrap.min.css',

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': None,
    # 'theme_url': 'https://maxcdn.bootstrapcdn.com/bootswatch/3.3.5/flatly
    # /bootstrap.min.css',
    # 'theme_url': 'https://maxcdn.bootstrapcdn.com/bootswatch/3.3.5/flatly/',

    # The complete URL to the Bootstrap JavaScript file (None means
    # derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant
    # if you use bootstrap3.html)
    'javascript_in_head': True,

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3
    # template tags)
    'include_jquery': True,

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

    # Class to indicate success, meaning the field has valid input
    # (better to set this in your Django form)
    'success_css_class': 'has-success',

    # Renderers (only set these if you have studied the source and
    # understand the inner workings)
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
