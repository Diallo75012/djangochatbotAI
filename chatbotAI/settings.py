import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
  "DJANGO_SECRET",
  'django-insecure-!n@d#_%6(7)gi6m)gc061b!rj)k6_1(q(@-apym6crmiuzji3+'
)

SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users.apps.UsersConfig',
    'businessdata.apps.BusinessdataConfig',
    'chatbotsettings.apps.ChatbotsettingsConfig',
    'common.apps.CommonConfig',
    'clientchat.apps.ClientchatConfig',
    'agents.apps.AgentsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware_logs_custom.CurrentUserMiddleware', # common app file `middleware_logs_custom.py` to have `user_id` automatically populated in logs
]
#] += ['common.middleware_logs_custom.CurrentUserMiddleware'] # common app file `middleware_logs_custom.py` to have `user_id` automatically populated in logs

ROOT_URLCONF = 'chatbotAI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'chatbotAI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# SQLite3 database default
"""
DATABASES = {
    'defacult': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# PostgresQL db custom
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.getenv("DBNAME"),
    'USER': os.getenv("DBUSER"),
    'PASSWORD': os.getenv("DBPASSWORD"),
    'HOST': os.getenv("DBHOST"),
    'PORT': os.getenv("DBPORT"),
  },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
# can be here the dir where also Nginx will serve django staticfiles
STATIC_ROOT = 'nginx/static'
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'static'),
]

# media root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL='media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10

}



# loggings: https://docs.djangoproject.com/en/4.1/topics/logging/#topic-logging-parts-formatters
'''

# logs formats 
'json'
'standard'
# Logs rotated every 7 days at midnight
'when': 'midnight',
'backupCount': 7,
# all logs centralized in django root project folder:
`logs/<app_name>.logs`
# all loggers writing to specific app log file and to master file:
 ['<app_name>_file', 'master_file', 'console']
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
      'user_id_filter': {
        '()': 'common.logs_filters.UserIDFilter',
      },
    },
    'formatters': {
        'json': {
            'format': (
                '{"time": "%(asctime)s",'
                ' "level": "%(levelname)s",'
                ' "name": "%(name)s",'
                ' "message": "%(message)s",'
                ' "user_id": "%(user_id)s"}'
            )
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'master_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'master.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
         # similarly for 'businessdata_file'... etc...
        'agents_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'agents.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
        'businessdata_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'businessdata.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
        'chatbotsettings_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'chatbotsettings.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
        'clientchat_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'clientchat.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
        'common_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'common.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
        'users_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'users.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
            'filters': ['user_id_filter'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {  # Root logger is `''`
            'handlers': ['master_file', 'console'],
            'level': 'DEBUG',
        },
        'agents': {
            'handlers': ['agents_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'businessdata': {
            'handlers': ['businessdata_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'chatbotsettings': {
            'handlers': ['chatbotsettings_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'clientchat': {
            'handlers': ['clientchat_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'common': {
            'handlers': ['common_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users': {
            'handlers': ['users_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },

    }
}
