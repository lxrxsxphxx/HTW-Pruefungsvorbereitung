# Backend

## Empfohlene VS Code Extension



## Konfigurationsreferenz


## Projekt Einrichtung

Python ([Download-Link](https://www.python.org/downloads/)) installieren, unter Linux idealerweise mit dem Package Manager.
Dann im Verzeichnis `backend` den folgenden Befehl ausführen

```sh
python -m venv .venv
```

Unter Windows dann bei Benutzung von CMD

```
.venv\Scripts\activate.bat
```

oder bei Benutzung von PowerShell

```
.venv\Scripts\Activate.ps1
```

oder unter Linux/MacOS

```sh
source .venv/bin/activate
```

die virtuelle Umgebung aktivieren und mit dem folgenen Befehl die benötigten Packages installieren

```sh
pip install -r requirements.txt
```

### Run and Hot-Reload for Development

Eine `.env` Datei nach dem Beispiel der `database/example.env` anlegen.
Falls die lokale Datenbank per Docker genutzt wird, kann die `.env` aus dem Verzeichnis `database` kopiert werden, als DB_HOST wird dann `localhost` eingetragen.

Um für die Entwicklung einen Server zu starten die virtuelle Umgebung aktivieren, falls nicht schon passiert, und den folgenden Befehl nutzen

```sh
fastapi dev app/main.py
```

Dieser Server lädt bei Speichern von Änderungen in Code automatisch die Änderungen direkt in die Webseite. Hot-Reload ist nicht immer perfekt, manchmal muss man auch einfach den Server neustarten.

## Entwicklung

Für die Entwicklung mit FastAPI stehen die [FastAPI Reference](https://fastapi.tiangolo.com/reference/) und die [FastAPI Tutorials](https://fastapi.tiangolo.com/tutorial) zur Verfügung. Für SQLModel gibt es die [SQLModel Tutorials](https://sqlmodel.tiangolo.com/tutorial/).
