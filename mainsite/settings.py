"""
Django settings for lcog project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from distutils.util import strtobool

import boto3
from storages.backends.s3boto3 import (S3Boto3Storage, S3StaticStorage) # Needed for staging/production static files

import logging

from dotenv import load_dotenv
load_dotenv()



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.getenv('DEBUG', 'True')))

SECURE_SSL_REDIRECT = bool(strtobool(os.getenv('USE_SSL', 'True')))
SESSION_COOKIE_SECURE = bool(strtobool(os.getenv('USE_SSL', 'True')))
CSRF_COOKIE_SECURE = bool(strtobool(os.getenv('USE_SSL', 'True')))

ENVIRONMENT = os.environ.get('ENVIRONMENT')

if ENVIRONMENT == 'STAGING': 
    ALLOWED_HOSTS = [
        'team-staging.lcog.org', # Staging frontend
        'api.team-staging.lcog.org', # Staging backend
        os.environ.get('EC2_PUBLIC_IP'), # Public IP of EC2 instance
        os.environ.get('EC2_PRIVATE_IP'), # Private IP of EC2 instance
        os.environ.get('EBS_DOMAIN'), # Domain of Elastic Beanstalk instance
    ]
else:
    # PRODUCTION
    ALLOWED_HOSTS = [
        'team.lcog.org', # Prod frontend
        'api.team.lcog.org', # Prod backend
        os.environ.get('EC2_PUBLIC_IP'), # Public IP of EC2 instance
        os.environ.get('EC2_PRIVATE_IP'), # Private IP of EC2 instance
        os.environ.get('EBS_DOMAIN'), # Domain of Elastic Beanstalk instance
    ]


# Application definition

INSTALLED_APPS = [
    'api',
    'mainsite',

    'deskreservation',
    'meals',
    'people',
    'purchases',
    'responsibilities',
    'timeoff',
    'workflows',
    
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'corsheaders',
    'ckeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'mainsite.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainsite.urls'

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

WSGI_APPLICATION = 'mainsite.wsgi.application'

# ASGI_APPLICATION = 'mainsite.asgi.application'
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Test SQLite DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    # TODO: Set up a local Postgres instance
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'iotd',
    #         'USER': 'iotd',
    #         'PASSWORD': 'iotd',
    #         'HOST': 'localhost',
    #         'PORT': '5432',
    #     }
    # }


# Development MySQL DB
# Production MySQL DB
# https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database#prerequisites
# NOT WORKING
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': '/etc/mysql/my.cnf',
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]

# Where to build static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# S3 storage bucket information
AWS_STORAGE_BUCKET_NAME = 'team-app-storage'
AWS_REGION_NAME = 'us-west-2'

# Tell django-storages the domain to use to refer to static files.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_DOMAIN = 'https://%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION_NAME)

# Static files (CSS, JavaScript, Images)
# Stored in AWS S3 bucket unless running locally
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = AWS_S3_DOMAIN

if 'STATICFILES_LOCATION' in os.environ:
    # Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
    # you run `collectstatic`).
    STATICFILES_LOCATION = os.environ['STATICFILES_LOCATION']
    MEDIAFILES_LOCATION = os.environ['MEDIAFILES_LOCATION']

    STORAGES = {
        "default": {
            "BACKEND": os.environ['DEFAULT_FILE_STORAGE'],
        },
        "staticfiles": {
            "BACKEND": os.environ['STATICFILES_STORAGE'],
        },
    }

# Set long timeout for static file browser caching
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

# LOGIN_REDIRECT_URL = '/dashboard'
# LOGOUT_REDIRECT_URL = '/dashboard'

#########
# Email #
#########

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

# EMAIL_BACKEND = 'django_ses.SESBackend'
# print('AWS_ACCESS_KEY_ID', os.environ.get('AWS_ACCESS_KEY_ID'))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('SES_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SES_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'no-reply@lcog.org'

# Required for django-ses
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = 'us-west-2'
# AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

###########
# LOGGING #
###########

AWS_LOG_GROUP = 'TeamAppLogGroup', # your log group
AWS_LOG_STREAM = 'TeamAppLogStream', # your stream
AWS_LOGGER_NAME = 'watchtower-logger' # your logger


boto3_logs_client = boto3.client("logs", region_name=AWS_REGION_NAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'aws': {
            # you can add specific format for aws here
            # if you want to change format, you can read:
            #    https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'watchtower': {
            'class': 'watchtower.CloudWatchLogHandler',
            'boto3_client': boto3_logs_client,
            'log_group_name': 'TeamAppLogGroup',
            'log_stream_name': 'TeamAppLogStream',
            # Decrease the verbosity level here to send only those logs to watchtower,
            # but still see more verbose logs in the console. See the watchtower
            # documentation for other parameters that can be set here.
            'level': 'DEBUG'
        }
    },
    'loggers': {
        AWS_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['watchtower'],
            'propagate': False,
        },
        # add your other loggers here...
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# Allow these addresses to access the Desk Reservation App
REST_FRAMEWORK_TRUSTED_IPS_LIST = []

# Frontend
if ENVIRONMENT == 'STAGING': 
    FRONTEND_DOMAIN = 'https://team-staging.lcog.org'
else:
    # Production
    FRONTEND_DOMAIN = 'https://team.lcog.org'

# Overwrite production settings with local ones
try:
    from .settings_local import *
except ImportError:
    pass