from time import sleep
from random import randint

class Charakter:
    def __init__(self, name, ist_kaempfer, ist_arbeiter, lebenspunkte):
        self.name = name
        self.fighter = ist_kaempfer
        self.worker = ist_arbeiter
        self.hp = lebenspunkte

class Arbeiter(Charakter):
    def __init__(self, name, ist_kaempfer, ist_arbeiter, lebenspunkte, geschick, ausdauer, kontrolle):
        Charakter.__init__(self, name, ist_kaempfer, ist_arbeiter, lebenspunkte)
        self.dex = geschick
        self.stam = ausdauer
        self.control = kontrolle

class Fischer(Arbeiter):
    def __init__(self, name, ist_kaempfer, ist_arbeiter, lebenspunkte, geschick, ausdauer, kontrolle, angelwert, anzahl_koeder, anzahl_fische, angelt):
        Arbeiter.__init__(self, name, ist_kaempfer, ist_arbeiter, lebenspunkte, geschick, ausdauer, kontrolle)
        self.aw = angelwert
        self.ak = anzahl_koeder
        self.af = anzahl_fische
        self.ang = angelt

    def angeln(self):
        if self.ak <= 0 or self.stam <= 0:
            print("Du hast keine Köder bzw. Ausdauer zum Fischen.")
            #return print(f"Anzahl Köder {self.ak} (-0) | Angelwert: {self.aw} (+0) | Ausdauer: {self.stam} (-0) | Fische: {self.af} (+0)")
            return
        else:
            self.ak -= 1
            self.stam -= 1
            print("Angel ausgeworfen!")
            sleep(2)
            fischgroesse = randint(1,30)
            angelwert = randint(1,3)
            if self.control + self.aw >= fischgroesse*2:
                self.aw += angelwert
                self.af += 2
                print(f"Du bist so gut im Fischen, dass du gleich zwei Fische mit einem Köder gefangen hast. Wie das geht? Wer weiß...\nDein Angelwert hat sich um {angelwert} verbessert.")
                return
            elif self.control + self.aw >= fischgroesse:
                self.aw += angelwert
                self.af += 1
                print(f"Du hast den Fisch gefangen. Dein Angelwert hat sich um {angelwert} verbessert.")
                return
                #return print(f"Anzahl Köder {self.ak} (-1) | Angelwert: {self.aw} (+{angelwert}) | Ausdauer: {self.stam} (-1) | Fische: {self.af} (+1)")
            else:
                if input("Der Fisch ist zu groß für deine Fähigkeiten. Möchtest du es trotzdem probieren? Bei Scheitern verlierst du die doppelte Ausdauer. [j]/[n] ").lower() == "j":
                    sleep(2)
                    if randint(0,2) != 0:
                        print(f"Du hast es trotz Erwarten geschafft! Dein Angelwert hat sich um {angelwert} verbessert.")
                        self.aw += angelwert
                        self.stam -= 1
                        self.af += 1
                        return
                        #return print(f"Anzahl Köder {self.ak} (-1) | Angelwert: {self.aw} (+{angelwert}) | Ausdauer: {self.stam} (-1) | Fische: {self.af} (+1)")
                    else:
                        print(f"Schade! Der Fisch ist entkommen und du verlierst 2 Ausdauerpunkte für den Tag, aber immerhin hat sich dein Angelwert um {angelwert} verbessert.")
                        self.aw += angelwert
                        self.stam -= 2
                        return
                        #return print(f"Anzahl Köder {self.ak} (-1) | Angelwert: {self.aw} (+0) | Ausdauer: {self.stam} (-2) | Fische: {self.af} (+0)")
                else:
                    #return print(f"Anzahl Köder {self.ak} (-1) | Angelwert: {self.aw} (+0) | Ausdauer: {self.stam} (-1) | Fische: {self.af} (+0)")
                    return

    def koeder_bauen(self):
        if self.stam > 0:
            if randint(1,2) == 1:
                print("Dein Geschick erhöht sich um 1!")
                self.dex +=1
            self.stam -= 1
            sleep(1)
            if randint(1,15) <= self.dex:
                self.ak += 2
                return print("Dein Geschick hat es dir erlaubt zwei Köder zu bauen!")
            else:
                self.ak += 1
                return print("Ein Köder wurde gebaut.")
        else:
            return print("Nicht genug Ausdauer.")

    def familie(self):
        sleep(1)
        x = randint(1,5)
        if x == 1:
            print("Du gehst nach Hause, um deine Frau zu überraschen. Aber dann erinnerst du dich, dass du gar keine hast, weil Angeln für dich dein Leben ist. (+5 Angelwert aus purem Trotz)")
            self.aw += 5
            return
        if x == 2:
            print("Du gehst deine Kinder besuchen... aber deine Kinder sind auch Fische. Da Moral keine Eigenschaft in diesen Spiel ist: +2 Fische.")
            self.af += 2
            return
        if x == 3:
            print("Du überlegst dir kurz, nach Hause zu gehen. Aber dann fällt dir ein, dass deine Familie darauf angewiesen ist, dass du sie mit Fischen am Leben erhaltest. (+2 Köder aus purer Motivation)")
            self.ak += 3
            return
        if x == 4:
            print("Du gehst nach Hause, aber keiner ist da. (Kein Effekt)")
        if x == 5:
            print("Du gehst nach Hause, und genießt deine Zeit mit der Familie. Du bist erfrischt. (+2 Ausdauer)")
            self.stam += 2
            return

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

