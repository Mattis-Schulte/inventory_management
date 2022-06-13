**Inventory Managment – Mattis Schulte, Sajan Sivapatham | [GitHub](https://github.com/Mattis-Schulte/inventory_management/)**



![Django](https://cdn.discordapp.com/attachments/882442489330540624/984725449034850325/ikea-django-logo.png)



- Inventory Managment
	- [Beschreibung des Projektes](#beschreibung)
	- [Aufgabenverteilung](#aufgabenverteilung)
	- [Gruppenmitglieder](#gruppenmitglieder)
	- [Der aktuelle Stand](#aktuellerstand)
	 	- [Grundfunktionen](#musthave)
	 	- [Erweitertefunktionen](#advanced)
	- [Besonderheiten](#besonderheiten)


<a name="beschreibung"></a>
## Beschreibung des Projektes
Unser Projekt beinhalt ein Programm, welches als Inventarmanagment-Tool für die Schule benutzt werden kann. Dabei sind viele nützliche Dinge enthalten wie z.B der itslearning-Login, das ansprechende und effiziente Design, die Vertiefung von denn einzelnen Programmbestandteilen usw.

<a name="aufgabenverteilung"></a>
## Aufgabenverteilung
In unserem Fall hat sich einer um die Erstellung des Projektes, die Zeitplanung, die Dokumentation des Projektes und Überlegungen zu denn Datenmodellen gemacht. Das andere Gruppenmitglied hat sich um die Gestaltung der Website, die Implementierung der einzelnen Bestandteile, Finalisierung der Datenmodelle usw. gekümmert. Viele Entscheidungen gingen dabei in Absprache mit dem anderen Gruppenmitglied, weshalb man bei manchen Projektteilen keine klare Grenze ziehen kann.

<a name="gruppenmitglieder"></a>
## Gruppenmitglieder
Folgende Gruppenmitglieder waren am Projekt beteiligt:
- Mattis Schulte
- Sajan Sivapatham

<a name="aktuellerstand"></a>
## Der aktuelle Stand
Der aktuelle Stand ist das die Grundfunktionen erfüllt sind und bei denn Erweiterungsfunktionen auch viele Extras miteingeflossen sind.

<a name="musthave"></a>
### Grundfunktionen
Alle Grundfunktionen sind enthalten. Folgende wurden uns gestellt:
- Räume
	- Räume hinzufügen inklusive Informationen
	- Räume entfernen
	- Räume anzeigen

- Geräte
	- Geräte hinzufügen
	- Geräte verschieben
	- Aktueller Status der Geräte

- Alle benutzten Geräte zeigen
- Räume mit Gerätenlisten anzeigen
- Verschiedene Filter
- Geräte mit Beschädigungen in einer Liste anzeigen
- Suchfunktion für Geräte und Räume
- Inventar aller Geräte anzeigen
- Hinweise zu denn Geräten anzeigen

- Standard-Admin:
	- User: admin
	- Passwort: Hallo12345



<a name="advanced"></a>
### Erweitertefunktionen
Zahlreiche Erweiterungen für unser Projekt sind:
- itslearning-Login (mit Übernahme von Rollen aus itslearning)
- Rechteverwaltung (Gäste, Schüler, Mitarbeiter, Admin, System-Admin), (Funktionsfähig: Wer kann Tickets hinzufügen, Rechte werden im Admin-Panel unter Gruppen eingestellt)
- Authentifizierung
- Daten-Export als CSV im Admin-Panel
- Ticket-System
- Darkmode
- Asynchrones Laden
- Innovatives und effektives Design
- Fehler und falsche Benutzereingaben werden korrekt behandelt
- Umfangreiche Filter
- Responsive Webdesign

<a name="besonderheiten"></a>
## Besonderheiten
Um das Projekt zu starten, muss man zuerst die `manage.py` Datei ausführen.
Dabei sollte man zuerst vom Stammordner mit dem Befehl `cd intern_szut` zu unserem Programmordner wechseln, um die `manage.py` Datei zu finden. Danach startet man die `manage.py` mit dem Befehl `python manage.py runserver --insecure`. Wenn man denn Befehl eingegeben hat, sollte sich ein Fenster im Browser öffnen, in dem das Programm dann erscheint.
