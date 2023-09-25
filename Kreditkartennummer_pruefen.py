#nummer = "9342571866701996"

nummer = input("16-stellige Kreditkartennummer? ")
summeQZ = 0
# Schritt 1: Verdopplung des Wertes jeder zweiten Ziffer, beginnend mit der vorletzten Ziffer
# Schritt 2: Summe der Quersummen

def QZverdoppelt(num):
    num = int(num)
    num = num * 2
    num = str(num)
    if len(num) == 1:
        return int(num)
    if len(num) == 2:
        return int(num[0]) + int(num[1])

for i in range(len(nummer)-2, -1, -1):
    if i % 2 == 0:
        summeQZ += QZverdoppelt(nummer[i])
    else:
        summeQZ += int(nummer[i])
print("Summe der Quernummern:", summeQZ)

# Schritt 3: Berechnung der Differenz zwischen dem Ergebnis aus Schritt 2 under nächst kleineren durch 10 teilbaren Zahl
schritt3 = summeQZ - (10*(summeQZ//10))
print("Ergebnis Schritt3:", schritt3)

# Schritt 4: Berechnung der Differenz zwischen 10 un dem Ergebnis aus Schritt 3. Ergibt sich als Differenz 10, wird diese auf 0 gesetzt.
if schritt3 == 10:
    pz = 0
else:
    pz = 10-schritt3

print("Prüfzahl:", pz)

if str(pz) == nummer[-1]:
    print("Nummer gültig")
else:
    print("Nummer nicht gültig")