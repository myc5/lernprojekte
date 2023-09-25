"""
Aufgabe: Zufällige Zahl von 0-300 generieren, Benutzer soll via Abfrage raten und Feedback erhalten (zu hoch,
zu niedrig, Zahl gefunden). Es soll auch die Anzahl der Versuch ausgegeben werden, wenn wir mit Raten fertig sind.
"""
#Import randrange
from random import randrange

# Variablen
startrange = 0
endrange = 301
rand_number = randrange(startrange, endrange)
count = 1
print(f"Es wurde eine Zahl zwischen {startrange} und {endrange-1} generiert. Kannst du Sie finden? ")

# Benutzerabfrage und Schleife

while True:
    guess = input("Bitte gebe eine Zahl an (-1 zum Abbrechen) ")
    while type(guess) != int:
        try:
            guess = int(guess)
        except ValueError:
            print("Das war gar keine Zahl.")
            guess = input("Bitte gebe eine Zahl an (-1 zum Abbrechen) ")
    if guess == rand_number:
        if count == 1:
            print("Wow, das war ja aber schnell! Gleich beim ersten Mal gefunden.")
        else:
            print(f"Du hast die Zahl gefunden! Du hast {count} Versuche gebraucht.")
        break
    elif guess == -1:
        if count == 1:
            print("Du hast nach einem Versuch abgebrochen.")
        else:
            print(f"Du hast nach {count} Versuchen abgebrochen.")
        break
    elif guess < rand_number:
        count += 1
        print("Deine eingegebene Zahl ist zu klein.")
    elif guess > rand_number:
        count +=1
        print("Deine eingegebene Zahl ist zu hoch.")
