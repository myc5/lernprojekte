IP_adresse = input("IP-Adresse? ")
sub = input("Subnetzmaske? ")
verbose = input("Mit Rechenweg? [j]oa / [n]joa ").lower()
print("-"*30)

# Debug
"""IP_adresse = "10.1.96.0"
sub = "255.255.240.0"
verbose = "j" """

count = 0

# Einlesen, Formatierung und Binärumwandlung der IP-Adressen
splitIP = IP_adresse.split(".")
okt1 = (8-len(bin(int(splitIP[0]))[2:]))*"0"+bin(int(splitIP[0]))[2:]
okt2 = (8-len(bin(int(splitIP[1]))[2:]))*"0"+bin(int(splitIP[1]))[2:]
okt3 = (8-len(bin(int(splitIP[2]))[2:]))*"0"+bin(int(splitIP[2]))[2:]
okt4 = (8-len(bin(int(splitIP[3]))[2:]))*"0"+bin(int(splitIP[3]))[2:]
oktkomplett = okt1+okt2+okt3+okt4

splitSub = sub.split(".")
subokt1 = (8-len(bin(int(splitSub[0]))[2:]))*"0"+bin(int(splitSub[0]))[2:]
subokt2 = (8-len(bin(int(splitSub[1]))[2:]))*"0"+bin(int(splitSub[1]))[2:]
subokt3 = (8-len(bin(int(splitSub[2]))[2:]))*"0"+bin(int(splitSub[2]))[2:]
subokt4 = (8-len(bin(int(splitSub[3]))[2:]))*"0"+bin(int(splitSub[3]))[2:]

suboktkomplett = subokt1+subokt2+subokt3+subokt4

# Zählen der "Binär-Einsen" für die CIDR
for i in suboktkomplett:
    if i == "1":
        count += 1

# Formatierung und das Addieren der Binärzahlen, damit man die im print anzeigen kann
addition = ""

list_suboktkomplett = list(suboktkomplett)
list_oktkomplett = list(oktkomplett)

for i in range(len(list_oktkomplett)):
    addition += str((int(list_oktkomplett[i])*int(list_suboktkomplett[i])))
    if i == 7 or i == 15 or i == 23:
        addition += "."

# Addition-Variable wird in Dezimal umgewandelt als Liste, damit man später die BC berechnen kann.
add1, add2, add3, add4 = int(addition[:8],2), int(addition[9:17],2), int(addition[18:26],2), int(addition[27:],2)
netzID = [add1, add2, add3, add4]


if count <= 8:
    oktett = 1

if 16 > count >= 9:
    oktett = 2

if 23 > count >= 15:
    oktett = 3

if count >= 24:
    oktett = 4

x = 2**(32-count)



if verbose == "j":
    print(f"IP-Adresse:                 {IP_adresse}")
    print(f"Sub-Adresse:               {sub}")
    print(f"Binär IP-Adresse:  {okt1}.{okt2}.{okt3}.{okt4}")
    print(f"Binär Sub-Adresse: {subokt1}.{subokt2}.{subokt3}.{subokt4}")
    print(f"Addition:          {addition}")
    print(f"CIDR-Suffix:                     / {count}")
    print(f"Netz-ID:               {add1}.{add2}.{add3}.{add4} / {count}")
    print(f"Blockgröße: 32 Bit - {count} Bit = {32-count} ==> 2^{32-count} Bit = {x}")
    print(f"Blockgröße (gesamt):", end=" ")

while x >= 256:
    if verbose == "j":
        print(f"{x}/256 =", end=" ")
    x = x // 256
    if verbose == "j":
        print(f"{x}", end="  ")

# Bestimmung der BC: +Blockgröße auf das x.te Oktett, dann -1 im 4.
bcNetz = netzID[:]
bcNetz[oktett-1] += x
if bcNetz[oktett-1] > 255:
    # bcNetz[oktett-2] += bcNetz[oktett - 1] - 255 Scheinbar gibt es keinen Übertrag? Stimmt das so?
    bcNetz[oktett - 1] = 255

if bcNetz[3] == 0:
    bcNetz[3] = 255
    if bcNetz[2] == 0:
        bcNetz[2] = 255
        if bcNetz[1] == 0:
            bcNetz[1] = 255
        else:
            bcNetz[2] = bcNetz[2] - 1
            if bcNetz[1] == 0:
                bcNetz[1] = 255
            else:
                bcNetz[1] = bcNetz[1] - 1
    else:
        bcNetz[2] = bcNetz[2] - 1
else:
    bcNetz[3] = bcNetz[3] - 1

if verbose == "j":
    print(f"({oktett}. Oktett)")
    print()

    print(f"                   {add1}  .  {add2}  .  {add3}  .  {add4}")
    if oktett == 4:
        print(f"                                      +{x}")
    elif oktett == 3:
        print(f"                               +{x}")
    elif oktett == 2:
        print(f"                         +{x}")
    elif oktett == 1:
        print(f"                  +{x}")
    print(f"                                      -1")
    print(f"Broadcast:         {bcNetz[0]}  .  {bcNetz[1]}  .  {bcNetz[2]}  .  {bcNetz[3]}")

print(f"Netz-ID: {netzID[0]}.{netzID[1]}.{netzID[2]}.{netzID[3]} / {count}")

print(f"Erste IP: {netzID[0]}.{netzID[1]}.{netzID[2]}.{netzID[3]+1}") # Was passiert bei 255 + 1? Übertrag oder nicht?
print(f"Letzte IP: {bcNetz[0]}.{bcNetz[1]}.{bcNetz[2]}.{bcNetz[3]-1}")

if verbose != "j":
    print(f"Broadcast: {bcNetz[0]}.{bcNetz[1]}.{bcNetz[2]}.{bcNetz[3]}")

print(f"Anzahl der möglichen Hosts: {2**(32-count) - 2}, Blockgröße: {x}")