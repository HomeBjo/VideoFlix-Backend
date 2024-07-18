# Videoflix Backend

## Anforderungen

- Python 3.8 oder höher
- PostgreSQL 12 oder höher

## Installation

1. **PostgreSQL installieren:**
   - Folge den Anweisungen auf der offiziellen PostgreSQL-Website für dein Betriebssystem: [PostgreSQL Downloads](https://www.postgresql.org/download/).

2. **Repository klonen und Abhängigkeiten installieren:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   python -m venv env
   source env/bin/activate  # Auf Windows: .\env\Scripts\activate
   pip install -r requirements.txt

3. **Erstelle eine .env-Datei im Projektverzeichnis:**
   Im Hauptverzeichnis des Projekts, erstelle eine neue Datei namens .env.
   Füge die folgenden Datenbankkonfigurationsparameter zur .env-Datei hinzu:
   DB_KEY=<Production-Key>
   DB_NAME=<Project-Name>
   DB_USER=<User-Name>
   DB_PASSWORD=<DB-Password>
   DB_HOST=<Server-Name>
   DB_PORT=<Port>

4. **Aktualisiere settings.py wie folgt:**
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
SECRET_KEY = config('DB_KEY'),
