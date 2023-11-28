# Eingabemaske

Programm zum Erfassen und Speichern von personenbezogenen Daten in einer GUI. 
Mit Option zum Speichern und Laden der Daten als "Person"-Objekt in einer JSON-Datei.

Ein Optionsmenü und Fehlererkennung für häufige Eingabefehler sind auch implementiert.

Features unter anderem:

- ID: Duplikate werden erkannt
- Vorname/Name: Autokorrektur für Capslock und Leerzeichen; Erkennung von Zahlen bzw. Sonderzeichen; optionale Blacklist 
- Geburtstag: Validiert korrektes Datum und ob es das berechnete Alter im erlaubten Bereich liegt (standardmäßig 13-100 J.)
- E-Mail: Prüft auf plausibel mögliche Eingaben, mit optionaler Whitelist und Blacklist für das Domain
- Geschlecht: Auswahl über Dropdown Menü
