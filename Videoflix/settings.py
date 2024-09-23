
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# css folder found
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if DEBUG:
   STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
else:
    STATIC_ROOT = '/var/www/html/static'
    
    
# Define the relative path to the videos
MEDIA_URL = '/media/'

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_ROOT = '/var/www/html/media'
    
    
    

# Define the relative path to the videos
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DB_KEY'),

# rest_framework Authentication
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'gruppe49345.developerakademie.org',
    'videoflix.xn--bjrnteneicken-jmb.de', 
    'videoflix.aleksanderdemyanovych.de'
]

# Django Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# rest_framework Authentication
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}


# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:8000",
    "http://127.0.0.1:4200",
    "http://127.0.0.1:8000",
    "http://gruppe49345.developerakademie.org",
    "https://videoflix.xn--bjrnteneicken-jmb.de",
    "https://videoflix.aleksanderdemyanovych.de",
]


# Application definition
AUTH_USER_MODEL = 'Users.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'Video_App.apps.VideoAppConfig',
    'Users',
    'corsheaders',
    'django_rq',
    'debug_toolbar',
    'import_export',
    'django_extensions',
]
#Import-Export
IMPORT_EXPORT_USE_TRANSACTIONS =  True


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Videoflix.urls'

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

WSGI_APPLICATION = 'Videoflix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Upload allow size 
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 # 10MB
# DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  #20MB

#Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}


#Redis
CACHES = {    
    "default": {        
        "BACKEND": "django_redis.cache.RedisCache",        
        "LOCATION": "redis://127.0.0.1:6379/1",        
        "OPTIONS": {   
            "PASSWORD": config('REDIS_PW'),   
            "CLIENT_CLASS": "django_redis.client.DefaultClient"        
        },        
        "KEY_PREFIX": "Videoflix"    
        }
    }

#Cash timer (15 minutes)
CACHE_TTL = 60 * 15

#Django RQ
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': config('REDIS_PW'), 
        'DEFAULT_TIMEOUT': 1000,
        # 'REDIS_CLIENT_KWARGS': {    # Eventual additional Redis connection arguments
        #     'ssl_cert_reqs': None,  # für auth bei redis
        # },
    },
    
    # ---->  BEI BEDARF DIE PRIO EINKOMMENTIEREN <----
    
    # 'with-sentinel': {    
    #     'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
    #     'MASTER_NAME': 'redismaster',
    #     'DB': 0,
    #     # Redis username/password
    #     'USERNAME': 'redis-user',
    #     'PASSWORD': 'secret',
    #     'SOCKET_TIMEOUT': 0.3,
    #     'CONNECTION_KWARGS': {  # Eventual additional Redis connection arguments
    #         'ssl': True
    #     },
    #     'SENTINEL_KWARGS': {    # Eventual Sentinel connection arguments
    #         # If Sentinel also has auth, username/password can be passed here
    #         'username': 'sentinel-user',
    #         'password': 'secret',
    #     },
    # },
    # 'high': {
    #      # MAIL BEI REGISTRIERUNG HIER REIN PACKEN --------------------------------------------------------
    #     'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
    #     'DEFAULT_TIMEOUT': 500,
    # },
    # 'low': {
    #     'HOST': 'localhost',
    #     'PORT': 6379,
    #     'DB': 0,
    # }
}

# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler'] # If you need custom exception handlers

# Email authentication
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = config('GMAIL_MAIL')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('GMAIL_MAIL')
EMAIL_HOST_PASSWORD = config('GMAIL_PW')

# 4h timer
PASSWORD_RESET_TIMEOUT = 14400

