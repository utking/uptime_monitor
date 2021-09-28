"""
Django settings for monitor project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ezud@c2m&x!p4kfr*w#wd962*@sh5)+!v^$4((*c!(e8odfx2r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'graphos',
    'django_mysql',
    'rest_framework',
    'apps.monitor',
    'apps.checks',
    'apps.schedule',
    'apps.runners',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'monitor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST':     '127.0.0.1',
#         'PORT':     '3306',
#         'NAME':     'monitor',
#         'USER':     'monitor',
#         'PASSWORD': 'monitor',
#         'OPTIONS': {
#             'charset':  'utf8mb4',
#         }
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   'dev_db.sqlite'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
BASE_URL = 'http://localhost:8000'

DEFAULT_CHECK_INTERVAL = 5

ALLOWED_CLIENT_SUBNETS = [
    '127.0.0.1/32',
]

USE_NOTIFICATIONS_QUEUE = False
NOTIFICATIONS_QUEUE_HOST = 'localhost'
NOTIFICATIONS_QUEUE_NAME = 'monitor'
NOTIFICATIONS_QUEUE_USER = 'rabbitmq'
NOTIFICATIONS_QUEUE_PASSWORD = 'rabbitmq'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_FROM = 'Uptime Monitor <no-reply@uptime.example.com>'
EMAIL_HOST_USER = 'user'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

JIRA_ENDPOINT = 'https://jira.example.com'
JIRA_USER_NAME = 'rest-api-user'
JIRA_USER_PASSWORD = 'rest-api-password'
JIRA_TRIGGERING_STATUS = 'CRITICAL'
JIRA_PRIORITY = 'Critical'
JIRA_TRANSITION_RESOLVED_ID = '511'
JIRA_RESOLUTION_ID = '0'
JIRA_POST_COMMENTS = False
JIRA_CLOSE_WHEN_RESTORE = True
JIRA_ISSUE_TYPE = 'Task'
JIRA_TYPE_OK = 'OK'

UI_ELEMENTS = {
    'ITEMS': [
        {'id': 'and', 'title': 'AND', 'is_parent': 1},
        {'id': 'or', 'title': 'OR', 'is_parent': 1},
        {'id': 'xpath', 'title': 'XPath root', 'is_parent': 1, 'has_url': 1, 'has_timeout': 1},
        {'id': 'get_value', 'title': 'Find an element and get its value', 'has_selector': 1, 'has_value': 1},
        {'id': 'set_value', 'title': 'Find an element and set its value', 'has_selector': 1, 'has_value': 1},
        {'id': 'get_text', 'title': 'Find an element and get its text', 'has_selector': 1, 'has_value': 1},
        {'id': 'wait', 'title': 'Wait for N seconds', 'type': 'setter', 'has_value': 1},
        {'id': 'click', 'title': 'Find an element and click on it', 'has_selector': 1},
        {'id': 'find', 'title': 'Find an element by its XPath', 'has_selector': 1},
        {'id': 'http_ping', 'title': 'HTTP(S) request', 'has_url': 1, 'has_timeout': 1},
    ]
}
