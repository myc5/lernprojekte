# lernprojekte

## Größere Projekte

## Eingabemaske

Programm zum Erfassen und Speichern von personenbezogenen Daten in einer GUI. 
Mit Option zum Speichern und Laden der Daten als "Person"-Objekt in einer JSON-Datei.

Ein Optionsmenü und Fehlererkennung für häufige Eingabefehler sind auch implementiert.

Features unter anderem:

- ID: Duplikate werden erkannt
- Vorname/Name: Autokorrektur für Capslock und Leerzeichen; Erkennung von Zahlen bzw. Sonderzeichen; optionale Blacklist 
- Geburtstag: Validiert korrektes Datum und ob es das berechnete Alter im erlaubten Bereich liegt (standardmäßig 13-100 J.)
- E-Mail: Prüft auf plausibel mögliche Eingaben, mit optionaler Whitelist und Blacklist für das Domain
- Geschlecht: Auswahl über Dropdown Menü

![qMTzgbp](https://github.com/myc5/lernprojekte/assets/136581584/64061859-d0e5-404d-9ab6-c80702459ebc)


## ITT-Net Helper
Die GUI-Version zur Bestimmung vom IPv4 Netz-IDs, Subnetzen usw.

### TO-DO:
- Implementierung von weiteren Module wie Transferzeiten und eventuell ein Quiz, das der User selbst anpassen kann.
- Fehlerbehandlung: Momentan gibt es noch keine Fehlermeldung bzw Korrektur, wenn eine Netzaddresse im falschen Format eingegeben wurde.
- Tooltips
- Design

Sample Screenshots:
![ITT-Helper Net Screenshot](https://github.com/myc5/lernprojekte/assets/136581584/c7a998c7-4b17-4236-a240-e1ed947cbff9)

![ITT-Helper Image Screenshot](https://github.com/myc5/lernprojekte/assets/136581584/8f24f729-315e-41db-b6d4-bb4ee1cf7508)


## Mittlere Projekte

### Fischer Spiel
Üben und arbeiten mit Klassen/OOP. War mehr als Spaßprojekt gedacht, deswegen bitte nicht zu ernst nehmen. Benötigt die game.py und fisher_classes.py im selben Ordner.

## Kleinere Projekte

### Prime Numbers (C++)
Printe alle Prime Nummern zwischen 0 und 100 aus.

### Base 10 Base 2 Conversion.py
Meine erste Programmidee. Konvertiert Base10 <-> Base2 (z.B. GiB in MB).

### Bisected Search Number Guessing
Übung für Binärsuche.

### Fibonacci und Fak mit Dictionary.py
Fibonacci (und Fakultät) rekursiv mit Dictionary.

### Fakultaet.py
Fakultät berechnen mit optionalem Rechenweg und Fehlerbehandlung bei der Eingabe

### Image Size Calculator.py
Berechnet die Größe einer Bild-Datei

### Kreditkartennummer_pruefen.py
Buchaufgabe: Prüfzahl einer Kreditkartennummer berrechnen lassen.

### Manual sorting as a function.py
Obwohl Python kann Elemente mit einer built-in Funktion sortieren, wollte ich eine manuelle Version davon erstellen, um mein Wissen zu vertiefen.

### Netzaddresse.py
Text-Version zur Berechnung von Netzaddressen.

### Text-Datei speichern und auslesen.py
Mit sys Textdatei speichern und auslesen lassen.

### Self defined max and min.py
Ähnlich wie **Manual sorting as a function.py**, eine built-in Funktion von Python für das eigene Verständnis selbst geschrieben.

### super.py
Benutzereingaben mit Fehlerbehandlung. Zur Nutzung als Import bei anderen Programmen oder ähnliches.

### Time converter.py
Sehr simples Programm, das Sekunden in volle Stunden, Minuten und Sekunden konvertiert.

### While Loop with Rerun Check + Number Check
Simpler Codeblock, um Benutzereingabe auf Fehler zu prüfen und/oder einen Loop so lange laufen zu lassen, bis der Benutzer es abbricht (z.B. für Programme bei denen man mehr Berechnungen hintereinander machen will)

### zahlErraten.py
Zufällige Zahl von 0-300 generieren, Benutzer soll via Abfrage raten und Feedback erhalten (zu hoch,
zu niedrig, Zahl gefunden). Es soll auch die Anzahl der Versuch ausgegeben werden, wenn wir mit Raten fertig sind.
