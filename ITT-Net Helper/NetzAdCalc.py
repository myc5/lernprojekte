def CIDR_to_sub(cidr_num):
    ci = {0: "0", 1: "128", 2: "192", 3: "224", 4: "240", 5: "248", 6: "252", 7: "254"}
    cidr_list = []
    if cidr_num >=1:
        subs_complete=cidr_num // 8
        subs_modulo = cidr_num % 8
        if subs_complete == 4:
            sub = "255.255.255.255"
            return sub
        for i in range(subs_complete):
            cidr_list.append("255")
        cidr_list.append(ci[subs_modulo])
        for i in range(4-len(cidr_list)):
            cidr_list.append("0")
    sub = cidr_list[0] + "." + cidr_list[1] + "." + cidr_list[2] + "." + cidr_list[3]
    return sub

def IP_split(IP_adresse):
    splitIP = IP_adresse.split(".")
    okt1 = (8-len(bin(int(splitIP[0]))[2:]))*"0"+bin(int(splitIP[0]))[2:]
    okt2 = (8-len(bin(int(splitIP[1]))[2:]))*"0"+bin(int(splitIP[1]))[2:]
    okt3 = (8-len(bin(int(splitIP[2]))[2:]))*"0"+bin(int(splitIP[2]))[2:]
    okt4 = (8-len(bin(int(splitIP[3]))[2:]))*"0"+bin(int(splitIP[3]))[2:]
    oktlist = (okt1+"."+okt2+"."+okt3+"."+okt4)
    return oktlist

def Sub_split(sub):
    splitSub = sub.split(".")
    subokt1 = (8-len(bin(int(splitSub[0]))[2:]))*"0"+bin(int(splitSub[0]))[2:]
    subokt2 = (8-len(bin(int(splitSub[1]))[2:]))*"0"+bin(int(splitSub[1]))[2:]
    subokt3 = (8-len(bin(int(splitSub[2]))[2:]))*"0"+bin(int(splitSub[2]))[2:]
    subokt4 = (8-len(bin(int(splitSub[3]))[2:]))*"0"+bin(int(splitSub[3]))[2:]
    suboktlist = (subokt1 +"."+ subokt2 +"."+ subokt3 +"."+subokt4)
    return suboktlist

def sub_to_CIDR(suboktlist):
    count = 0
    for i in suboktlist:
        if i == "1":
            count += 1
    return count

def block_size(count):
    block_size = 2 ** (32 - count)
    while block_size >= 256:
        block_size = block_size//256
    return block_size

def oktett(count):
    if count <= 8:
        oktett = 1

    if 16 >= count >= 9:
        oktett = 2

    if 24 >= count >= 17:
        oktett = 3

    if count >= 25:
        oktett = 4
    return oktett

def network_class(addition):
    first_octet = addition[:4]
    if first_octet == "1111":
        type = "Class E Network"
    elif first_octet == "1110":
        type = "Class D Network"
    elif first_octet == "1100":
        type = "Class C Network"
    elif first_octet == "1000":
        type = "Class B Network"
    elif first_octet == "0000":
        type = "Class A Network"
    return type

def netzIDlist(addition):
    add1, add2, add3, add4 = int(addition[:8],2), int(addition[9:17],2), int(addition[18:26],2), int(addition[27:],2)
    netzID = [add1, add2, add3, add4]
    return netzID

def binary_add(oktlist, suboktlist):
    addition = ""
    list_suboktkomplett = list(suboktlist)
    list_oktkomplett = list(oktlist)
    for i in range(len(list_oktkomplett)):
        try:
            addition += str((int(list_oktkomplett[i])*int(list_suboktkomplett[i])))
        except ValueError:
            addition += "."
    return addition

def broadcastIP(netzID, oktett, block_size):
    bcNetz = netzID[:]

    bcNetz[oktett - 1] += block_size
    bcNetz[3] -= 1

    # carryover from okt4 to 3
    if bcNetz[3] == 0 or bcNetz[3] == -1:
        bcNetz[3] = 255
        bcNetz[2] -= 1
        if bcNetz[2] == 0 or bcNetz[2] == -1:
            bcNetz[2] = 255
            bcNetz[1] -= 1
            if bcNetz[1] == 0 or bcNetz[1] == -1:
                bcNetz[1] = 255
                bcNetz[0] -= 1
    broadcast_IP = str(bcNetz[0]) + "." + str(bcNetz[1]) + "." + str(bcNetz[2]) + "." + str(bcNetz[3])
    first_IP = str(netzID[0]) + "." + str(netzID[1]) + "." + str(netzID[2]) + "." + str(netzID[3] + 1)
    last_IP = str(bcNetz[0]) + "." + str(bcNetz[1]) + "." + str(bcNetz[2]) + "." + str(bcNetz[3] - 1)
    return broadcast_IP, first_IP, last_IP

# Debug
debug = False
if debug:
    IP_adresse = "10.0.0.253"
    #sub = "255.255.255.192"
    cidr_input = 22
    sub = CIDR_to_sub(cidr_input)

    """
    print("Subnetzmaske", sub, end=", ")
    print("Typ:", network_class(cidr_input))"""

    print("IP-Adresse", IP_adresse)
    print("Subnetzmaske", sub)

    oktlist=IP_split(IP_adresse)
    suboktlist=Sub_split(sub)
    addition = binary_add(oktlist, suboktlist)
    netzID = netzIDlist(addition)
    cidr = sub_to_CIDR(suboktlist)

    print("Binäre Netzadresse:   ", oktlist)
    print("Binäre Subnetzmaske: +", suboktlist)
    print(22*" ", 35*"-")
    print("Binäre Addition:", 5*" ", addition)
    print("CIDR: ", cidr)
    print(f"Netz-ID: {netzID[0]}.{netzID[1]}.{netzID[2]}.{netzID[3]}")
    print(f"Oktett: {oktett(cidr)}")
    #print(f"{block_size(cidr)}")
    block_size = block_size(cidr)
    broadcastIP(netzID, oktett(cidr), block_size)
    print(f"Anzahl Hosts: {2**(32-cidr)-2}")




