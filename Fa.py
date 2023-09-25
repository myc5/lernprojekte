from time import sleep
welcome = "Dieses Programm berechnet die Fakultät n! für eine positive, ganze Zahl. \n"
acceptableNumber = False
showTheMath = False
n = ""

print(welcome)

"""
Schleife der Benutzerfrage läuft so lange ab, bis wir keinen String, Float oder negative Zahl erkennen.
"acceptableNumber" hilft uns dabei, da man diese Variable später auf True setzen können, wenn 
wir einen Integer erkennen.
"""

while not acceptableNumber:
    # Floatkonversion, damit wir eine spezifische Fehlermeldung dafür geben können, ansonsten wäre
    # Integerkonversion hier die einfachere Wahl.
    try:
        n = float(input("Bitte gebe eine Zahl zur Berechnung an: "))
    except ValueError:
        # Das soll nur ausgeben werden, wenn ein String eingeben wurde. Deshalb der isinstance check.
        if isinstance(n, str):
            print("Es wurde keine gültige Zahl eingegeben.\n")
    # Wenn eine Zahl eingeben wurde, gibt es mehrere Möglichkeiten, was es sein kann.
    if type(n) == float:
        # Wenn 1 oder 0 eingegeben wurde, müssen wir erst gar nicht rechnen. Ergebnis ist immer 1.
        if n == 0.0 or n == 1.0:
            # Typkonversion, damit das Print besser aussieht (sonst steht da 1.0! ist 1.)
            n = int(n)
            print(f"{n}! ist 1.")
            break
        # Hier gucken wir, ob wir das float zum Integer ohne Informationsverlust machen können.
        # Option 1: Es geht nicht, da nicht glatt durch 1 teilbar, dann gibt es den Fehlertext hier.
        elif n % 1 != 0:
            print(f"Leider funktioniert dieses Programm nur mit ganzen Zahlen. \n")
        # Option 2: Es geht, also konvertieren wir.
        if n % 1 == 0:
            n = int(n)
            # Ist n negativ, dann geht Fakultät aus mathematischen Gründen nicht.
            if n < 0:
                print("Die Fakultätsfunktion ist nur mit positiven Zahlen möglich.\n")
            # Ist n eine ganze, positive Zahl (und nicht 0 oder 1), können wir endlich
            # mit dem Rechnen anfangen.
            if n > 0:
                acceptableNumber = True
# Soll der Rechenweg gezeigt werden?
if acceptableNumber:
    print("")
    question = input("Soll der Rechenweg gezeigt werden? [j/n]")
    print("")
    if question == "j":
        showTheMath = True
        # Es ist ne Pause eingebaut zwischen jeder gezeigten Zahl.
        # Damit das bei großen n's nicht zu lange dauert, kürzen wir die Pausen.
        if n >= 30:
            t = 5/10
        elif n >= 20:
            t = 7/10
        elif n <= 10:
            t = 10/10
# Die Rechnung: n * n(-1) * (n-2) etc.
if n > 1:
    fak2 = n
    for i in range(1, n):
        fak2 = fak2*i
        # Rechenwegabschnitt Start
        if showTheMath:
            print(i, end="*")
            sleep(t)
    if showTheMath:
        print(f"{n} = {fak2}\n")
        sleep(t)
        # Rechenwegabschnitt Ende
    print(f"{n}! ist {fak2}.")