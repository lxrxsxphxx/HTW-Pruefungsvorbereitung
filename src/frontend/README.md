# Frontend

## Empfohlene VS Code Extension

[Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) ist die von Vue.js selbst empfohlene VS Code Extension, die Installation ist also sehr sinnvoll.

## Konfigurationsreferenz

Für die Konfiguration von Vite (Webserver, der das Vue Projekt bereitstellt) kann in der [Vite Configuration Reference](https://vite.dev/config/) nachgelesen werden, wie man etwas konfiguriert.

## Projekt Einrichtung

Node.js ([Download-Link](https://nodejs.org/en/download)) installieren, nicht mit Docker, unten gibt es für Windows/MacOS einen Installer, Linux idealerweise mit dem Package Manager. Dann im Verzeichnis `frontend` den folgenden Befehl ausführen

```sh
npm install
```

### Compile and Hot-Reload for Development

Um für die Entwicklung einen Webserver zu starten den folgenden Befehl nutzen

```sh
npm run dev
```

Dieser Server lädt bei Speichern von Änderungen in Code automatisch die Änderungen direkt in die Webseite. Hot-Reload ist nicht immer perfekt, manchmal muss man auch einfach den Server neustarten.

### Compile and Minify for Production

Um das Projekt für das Deployment zu bauen, wird der folgende Befehl verwendet

```sh
npm run build
```

## Entwicklung

Als Ressourcen für die Entwicklung stehen von Vue [Vue Guide](https://vuejs.org/guide/introduction.html) für Vue allgemein und [Vue Router Guide](https://router.vuejs.org/guide/) für Vue Router zur Verfügung.
Zusätzlich ist im bereits erstellten Basis Projekt ein kleines Beispiel zu sehen, wie man Vue und Vue Router verwendet.
