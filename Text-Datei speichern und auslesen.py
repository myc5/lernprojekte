import sys

pfad = input("In welche .txt-Datei soll gespeichert werden? Leer lassen, um in der Default-Datei zu speichern: ")
if pfad != "":                # Wenn die .txt-Endung bei der Eingabe vergessen wurde, wird sie hier eingefügt.
    if pfad.find(".txt") == -1:
        pfad += ".txt"

zeilenAnzahlSchreiben = int(input("Wie viele Zeilen sollen eingegeben werden? "))
text = []

for i in range(zeilenAnzahlSchreiben):
    inp = input(f"Zeile {i+1} von {zeilenAnzahlSchreiben}: ")
    text.append(inp)
    text.append("\n")                   # Hier wird der Zeilenumbruch erzwungen.

try:
    if pfad == "":                     # Überprüfen, ob irgendwas eingegeben wurde. Falls nicht, benutze den default.
        file = open("Beispiel.txt", "w")
    else:
        file = open(pfad, "w")
    file.writelines(text)
    file.close()
    print("")
    print("Der Text wurde erfolgreich gespeichert.")
except IOError:
    print("Datei konnte nicht geöffnet werden.")
except:
    print("Es ist folgender Fehler ausgetreten:", sys.exc_info()[0])

print("")

zeilenAnzahlLesen = int(input("Wie viele Zeilen sollen ausgegeben werden? "))
if pfad == "":
    file = open("Beispiel.txt", "r")
else:
    file = open(pfad, "r")
text = file.readlines()

for line in text:
    zeilenAnzahlLesen -=1
    print(line.strip())   # .strip, um den Zeilenumbruch (\n) zu entfernen, sonst bekommt man leere Zeilen im Ergebnis.
    #print(line)
    if zeilenAnzahlLesen == 0:
        break
file.close()

