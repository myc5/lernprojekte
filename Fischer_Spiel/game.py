from player_classes import Fischer, bcolors
from random import randrange
from time import sleep

ausdauer, geschick, kontrolle = 3, 3, 3
instructions = True

player_name = input("Willkommen zu World of Fish of Fishcraft. Welchen Namen soll dein Charakter haben? ")
print()
print(f'"{player_name}"? Na dann.')
print()
player_choice = input("Welche Klasse möchtest du erstellen? Du kannst auswählen zwischen [F]ischer, [F]ischer und [F]ischer: ").lower()
print()

if player_choice == "f":
    print(f"Gute Wahl, deine Klasse ist der mächtige Fischer! Dieser verfügt über diese Attribute:\n{bcolors.OKCYAN}[G]eschick{bcolors.ENDC}\n{bcolors.OKGREEN}[A]usdauer{bcolors.ENDC}\n{bcolors.WARNING}[K]ontrolle{bcolors.ENDC}")
else:
    print(f'Hast du die "F"-Taste verfehlt? Es gibt hier nur Fischer, Kinder von Fischern und Fische. Und als Fisch spielen ist leider in allen Bundesländern außer Sachsen verboten.\n \nDeshalb wirst du zum Fischer. Dieser verfügt über diese Attribute:\n{bcolors.OKCYAN}[G]eschick{bcolors.ENDC}\n{bcolors.OKGREEN}[A]usdauer{bcolors.ENDC}\n{bcolors.WARNING}[K]ontrolle{bcolors.ENDC}')

while instructions:
    print()
    instructions_choice = input("Falls du herausfinden möchtest, welches Attribut was macht, drücke die entsprechende Taste. Ansonsten drücke [W] für weiter. ").lower()
    if instructions_choice == "w":
        instructions = False
    if instructions_choice == "g":
        print("Geschick verbessert die Chance, die doppelte Anzahl von Ködern herzustellen. Köder zu bauen hat eine Chance diesen Wert zu verbessern.")
        print()
    if instructions_choice == "a":
        print("Ausdauer bestimmt wie viele Aktionen man am Tag bekommt. Dieses ist ein sehr wichtiges Attribut.")
        print()
    if instructions_choice == "k":
        print("Kontrolle erlaubt größere Fische zu fangen, ohne es auf Glück ankommen zu lassen. Dein Angelwert verbessert dieses Attribut während des Spiels.")
        print()

sleep(1)
print()
print(f"Die Fähigkeitswerte werden jetzt zufällig ausgewürfelt, du kannst sie aber beliebig zuordnen. {bcolors.BOLD}Beachte: Ausdauer ist sehr wichtig.{bcolors.ENDC}")
print()

attributes = [randrange(4, 10) for i in range(3)]
sleep(1)
print(f"Folgende Attribute stehen zur Verfügung: {attributes}")
sleep(3)
print()
if input("Möchtest du die Attribute nochmal ausrollen lassen? [j]/[n] ").lower() == "j":
    sleep(1)
    print()
    print("Überprüfe DLC Status...")
    print()
    sleep(2)
    input(f"{bcolors.FAIL}Pay-to-Win Modul nicht gefunden.{bcolors.ENDC} Fortfahren ohne neu auszurollen? [j]a/[y]es/[s]i/[o]ui/[n]atürlich ")
    print()
    print("Gute Wahl.")

print()
for i in range(3):
    x = input(f"{attributes[i]} soll welcher Eigenschaft zugeordnet werden? {bcolors.OKCYAN}[G]eschick{bcolors.ENDC}, {bcolors.OKGREEN}[A]usdauer{bcolors.ENDC} oder {bcolors.WARNING}[K]ontrolle{bcolors.ENDC}? ").lower()
    print()
    if x == "g":
        geschick = attributes[i]
    elif x == "a":
        ausdauer = attributes[i]
    elif x == "k":
        kontrolle = attributes[i]
sleep(1)
print()
print("Dein Ziel ist es, 5 Tage zu überleben. Fange dafür mindestens 3 Fische am Tag, ansonsten ist es Game Over.")
print()
print("Mit welchem Schwierigkeitsgrad möchtest du spielen?")
print()
difficulty = input('[1] "An welcher Seite der Angel befestige ich den Köder?" (Easy: +5 Ausdauer, +5 Köder, +5 Fische)\n[2] "Ich hab schon mal ein Tutorialvideo übers Angeln geguckt" (Medium: +3 Ausdauer, +3 Köder, +3 Fische)\n[3] "Ich bin der Angelgott!" (Hard: +1 Ausdauer, +1 Köder, +1 Fisch)\n[4] "Meine Schwiegermutter ist halb Angelfisch" (Very Hard, keine Boni, nur Beileidswünsche)\n -> ')
print()

anzahl_koeder, anzahl_fische = 0, 0

if difficulty == "1":
    ausdauer += 5
    anzahl_koeder, anzahl_fische = 5, 5
    difficulty_name = "Easy"
elif difficulty == "2":
    ausdauer += 3
    anzahl_koeder, anzahl_fische = 3,3
    difficulty_name = "Medium"
elif difficulty == "3":
    difficulty_name = "Hard"
    ausdauer += 1
    anzahl_koeder, anzahl_fische = 1, 1
elif difficulty == "4":
    difficulty_name = "Angelfisch"
else:
    difficulty_name = difficulty


#name, ist_kaempfer, ist_arbeiter, lebenspunkte, geschick, ausdauer, kontrolle, angelwert, anzahl_koeder, anzahl_fische, angelt)
fisher = Fischer(player_name, False, True, 10, geschick, ausdauer, kontrolle, 1, anzahl_koeder, anzahl_fische, False)
#fisher = Fischer("Bob the Fisher", False, True, 10, 5, 10, 5, 5, 0, 15, False)
#stam_OG = 10
d = 1
g = len(fisher.name) + 47
h = 5
family_flag = True
stam_OG = ausdauer
game = True

while game:
    print(f"-" * g);
    print(f"| {bcolors.BOLD}{fisher.name}{bcolors.ENDC} |", end=" "); print(f"{bcolors.OKCYAN}Geschick: {fisher.dex}{bcolors.ENDC} | {bcolors.OKGREEN}Ausdauer: {fisher.stam}{bcolors.ENDC} | {bcolors.WARNING}Kontrolle: {fisher.control}{bcolors.ENDC} |")
    print("-" * g)
    print(f"---------------\n| {bcolors.UNDERLINE}Tag {d} von 5{bcolors.ENDC} |\n---------------")
    print()
    print(f"*** {bcolors.OKCYAN}Anzahl Köder: {fisher.ak}{bcolors.ENDC} | Angelwert: {fisher.aw} | {bcolors.OKGREEN}Ausdauer: {fisher.stam}{bcolors.ENDC} | {bcolors.WARNING}Fische: {fisher.af}{bcolors.ENDC} | {bcolors.FAIL}Modus: {difficulty_name}{bcolors.ENDC} ***")
    print()
    print("Oh mächtiger Fischer, was möchtest du tun?\n[1] Fischen gehen (-1 Ausdauer, Fisch Chance)\n[2] Zeit mit der Familie verbringen (+???)\n[3] Köder bauen (-1 Ausdauer/+1 Köder)}\n[4] Schlafen (Ausdauer erfrischen, -3 Fische, +1 Tag)\n[Q] Exit")
    while True:
        game_step = input("-> ")
        if game_step == "1":
            fisher.angeln()
        elif game_step == "2":
            if family_flag:
                fisher.familie()
                family_flag = False
            else:
                print("Das geht nur einmal pro Tag.")
        elif game_step == "3":
            fisher.koeder_bauen()
        elif game_step == "4":
            if fisher.af >= 3:
                fisher.af -= 3
                d += 1
                family_flag = True
                fisher.stam += stam_OG
                if fisher.stam > stam_OG:
                    fisher.stam = stam_OG
                print("Du gehst nach Hause. Deine Familie freut sich über die gefangenen Fische und du wachst erfrischt auf.")
                break
            else:
                if fisher.stam <= 0:
                    print(f"{bcolors.FAIL}Oh je, du hast nicht genügend Fische, um zum nächsten Tag fortzuschreiten, aber auch nicht genügend Ausdauer, um Fischen zu gehen...{bcolors.ENDC}")
                    print(f"{bcolors.FAIL}Wegen Dir verhungern deine Kinder, deine Frau verlässt dich und du beschließt dich den Quellcode zu lesen, damit dies nicht nochmal passiert.{bcolors.ENDC}")
                    print(f"{bcolors.BOLD}{bcolors.FAIL}Spiel beendet.{bcolors.ENDC}{bcolors.ENDC}")
                    game = False
                    break
                print("Du brauchst mindestens 3 Fischen, um Schlafen zu gehen. Geh Fischen!")

        elif game_step in ("q", "Q"):
            game = False
            break
        else:
            print(f"Befehl '{game_step}' ist erst im DLC möglich.")
        print()
        print(f"{bcolors.OKCYAN}Anzahl Köder: {fisher.ak}{bcolors.ENDC} | Angelwert: {fisher.aw} | {bcolors.OKGREEN}Ausdauer: {fisher.stam}{bcolors.ENDC} | {bcolors.WARNING}Fische: {fisher.af}{bcolors.ENDC}")
        #print(f"Anzahl Köder: {fisher.ak} | Angelwert: {fisher.aw} | {bcolors.OKGREEN}Ausdauer: {fisher.stam} | Fische: {fisher.af}")
    if d == 6:
        print(f"{bcolors.BOLD}Game Over.{bcolors.ENDC}", end=" ")
        if fisher.af == 1:
            print(f"Du hast es geschafft alle Tage zu überleben, mit einem Fisch übrig.")
        else:
            print(f"Du hast es geschafft alle Tage zu überleben, mit {fisher.af} Fischen übrig.")
        game = False
print()
input("Mit beliebiger Taste Fenster schließen.")
