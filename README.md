# Videoflix Backend

## Anforderungen

- Python 3.8 oder höher
- PostgreSQL 12 oder höher
- FFmpeg
- Redis

## Installation

1. **PostgreSQL installieren:**
   - Folge den Anweisungen auf der offiziellen PostgreSQL-Website für dein Betriebssystem: [PostgreSQL Downloads](https://www.postgresql.org/download/).

2. **FFmpeg installieren:**
   - Folge den Anweisungen auf der offiziellen FFmpeg-Website für dein Betriebssystem: [FFmpeg Downloads](https://ffmpeg.org/download.html).   

3. **Redis installieren:**
   - Folge den Anweisungen auf der offiziellen Redis-Website für dein Betriebssystem: Redis Downloads.  

4. **Repository klonen und Abhängigkeiten installieren:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   python -m venv env
   source env/bin/activate  # Auf Windows: .\env\Scripts\activate
   pip install -r requirements.txt

5. **Erstelle eine .env-Datei im Projektverzeichnis:**
   Im Hauptverzeichnis des Projekts, erstelle eine neue Datei namens .env.
   Füge die folgenden Datenbankkonfigurationsparameter zur .env-Datei hinzu:
   DB_KEY=<Production-Key>
   DB_NAME=<Project-Name>
   DB_USER=<User-Name>
   DB_PASSWORD=<DB-Password>
   DB_HOST=<Server-Name>
   DB_PORT=<Port>

6. **Aktualisiere settings.py wie folgt:**
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
            "PASSWORD": "foobared", # for example pw 
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
        'PASSWORD': 'foobared', # for example pw
        'DEFAULT_TIMEOUT': 360,
        # 'REDIS_CLIENT_KWARGS': {   
        #     'ssl_cert_reqs': None,  
        # },
    },
    }

IMPORT_EXPORT_USE_TRANSACTIONS =  True
STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')




7. **Migrationen erstellen und anwenden:**
   python manage.py makemigrations
   python manage.py migrate

8. **Statische Dateien sammeln:**
   python manage.py collectstatic

9. **RQ Worker starten:**
   python manage.py rqworker default

10. **Statische Dateien sammeln:**
   python manage.py runserver
   