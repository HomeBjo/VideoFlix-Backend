# Videoflix Backend

## Requirements

- Python 3.8 oder höher
- PostgreSQL 12 oder höher
- FFmpeg
- Redis

## Installation

1. **Install PostgreSQL:**
   - Follow the instructions on the official PostgreSQL website for your operating system: [PostgreSQL Downloads](https://www.postgresql.org/download/).

2. **Install FFmpeg:**
   - Follow the instructions on the official FFmpeg website for your operating system: [FFmpeg Downloads](https://ffmpeg.org/download.html).   

3. **Install Redis:**
   - Follow the instructions on the official Redis website for your operating system: Redis Downloads. 

4. **Clone repository and install dependencies:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   python -m venv env
   source env/bin/activate  # For windows: .\env\Scripts\activate
   pip install -r requirements.txt

5. **Create an .env file in the project directory:**
   <!-- In the main directory of the project, create a new file called .env .
   Add the following database configuration parameters to the .env file: -->
   DB_KEY=<Production-Key>
   DB_NAME=<Project-Name>
   DB_USER=<User-Name>
   DB_PASSWORD=<DB-Password>
   DB_HOST=<Server-Name>
   DB_PORT=<Port>
   REDIS_PW=<Your-Password>
   GMAIL_MAIL=<Your-Gmail(or-another-provider)-Account>
   GMAIL_PW=<Your-Gmail-Password>

6. **Update settings.py as follows:**
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

   SECRET_KEY = config('DB_KEY')

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


   RQ_QUEUES = {
      'default': {
         'HOST': 'localhost',
         'PORT': 6379,
         'DB': 0,
         'PASSWORD': config('REDIS_PW'),
         'DEFAULT_TIMEOUT': 360,
      }
   }

   IMPORT_EXPORT_USE_TRANSACTIONS =  True
   STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')

   #Email authentication
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com' <!-- add here your provider -->
   EMAIL_FROM = config('GMAIL_MAIL')
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = config('GMAIL_MAIL')
   EMAIL_HOST_PASSWORD = config('GMAIL_PW')

7. **Create and apply migrations:**
   python manage.py makemigrations
   python manage.py migrate

8. **Collect static files:**
   python manage.py collectstatic

9. **Start RQ Worker:**
   python manage.py rqworker default

   <!--
   If you use Windows and the rq-winworker doesn't work for you, then try the following:
   - Installiere ubunto und verknüpfe das mit windows. 
   - Start in VSCode das projekt and a second wsl shell(bash/pwsh). 
   - Now navigate to the project and install the env (now you have two env. One from windows and one from linux)
   - Install your requirements(from requirements.txt)
   - Start now your server via windows and the rq-worker via linux
   The rq-worker should now run under windows. Also make sure that the connection to redis is established.
   -->

10. **Start the server:**
   python manage.py runserver
   