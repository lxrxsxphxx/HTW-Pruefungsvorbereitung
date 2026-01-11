# Bruno Testclient
Für die Integrationstests wird der Bruno Client benutzt.

[usebruno.com](https://docs.usebruno.com/)

Aus dem Manifest:

_"We refuse to be shoehorned into a proprietary version control system for collaborating on API collections and we don’t want the details of our APIs, API requests, or API responses synced to the cloud and potentially be made public._

_We are an opensource project, rising up against the monopoly of bloated and closed systems. We believe that API collections should be co-located within your source code repository, serving as a living set of examples on how to use the API."_

Bruno ist ein Open-Source API Client, der sich klar als Alternative zu Postman positioniert.

# Bruno Installation

Bruno wie auf der Website beschrieben installieren.

Es sollte *nicht* die snap Installation durchgeführt werden, da diese bei der Benutzung des CLI später Probleme machen kann.

https://docs.usebruno.com/bruno-basics/download

# Installation Bruno CLI
Das Command Line Interface (CLI) ist für die Ausführung der Collection interessant.

Für die Installation ein Package Manager gebraucht. Wir benutzen npm. Es sollte vorher sichergestellt sein, dass Node.js auf dem System installiert ist.

Danach:

```sh
npm install -g @usebruno/cli
```

Um zu testen, ob die Installation erfolgreich war:

```sh
bru run --version
```

Eine Auflistung möglicher flags lässt sich anzeigen mit:

```sh
bru run -h
```

Um die Collection auszuführen, müssen Datenbank und Backend laufen. Die Informationen dazu finden sich in den README.md Dateien in `/database` und `/backend`.

Dann:
Wechsel in das Verzeichnis `/testing/testing_backend`
Dieses Verzeichnis ist die Collection. 

Anschließend

```sh
bru run --reporter-html ../reports/report.html
```

Dieser Befehl führt die Collection aus und erstellt einen report im Ordner `/reports`

Der report kann auch in anderen Dateiformaten erstellt werden: 
* json
* junit

Die Dateiendungen müssen dementsprechend angepasst werden.

# Kurzabriss Benutzung Bruno Client
Bruno organisiert Requests als sogenannte Collections. Eine Collection ist ein Ordner, in dem die Requests gespeichert werden. In einer Collection können die Request auch durch weitere Ordner gebündelt werden.

Die grafische Oberfläche bietet die Möglichkeit, Requests zu erstellen und bequem umzusortieren. Wählt man eine Request in einer Collection aus, gibt es verschiedene Menüs. Die folgenden Menüs sind für dieses Projekt relevant:
* Params: Festlegung und Verwaltung von Query und Pfadvariablen.
* Body: Festlegung des Body-Inhalt der Request.
* Script: Implementierung von Skripten. Es gibt Pre- und Post-Request Skripte. Diese werden vor allem benutzt um Runtime Variablen anzulegen.
* Assert: Definition von Asserts für einfache Tests.

# Mögliche Probleme
Fehler:
```sh
You can run only at the root of a collection
```

Lösung: Das Working Directory ist nicht das Verzeichnis der Collection, deshalb muss in die Collection gewechselt werden.

---

Fehler:
Riesige Wand aus Errors

Grund: Vermutlich wurde Bruno mit snap installiert. Das führt auf vielen Systemen zu Problemen.

Lösung: 
```sh
snap remove bruno
```
Anschließend erneut installieren, Anleitung dafür auf der Website.