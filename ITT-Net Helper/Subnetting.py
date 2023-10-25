network_ID = [192, 168, 1, 0]
CIDR = 26
num_of_subnets = 8
list_of_net_IDs = []
list_of_first_IPs = []
list_of_last_IPs = []
list_of_bc_IPs = []
CIDR_dict = {2:1, 4:2, 8:3, 16:4, 32:5, 64:6, 128:7, 256:8, 512:9, 1024:10}

#last IPs/bc wrong

def subnet_net_IDs(network_ID, CIDR, num_of_subnets):
    new_CIDR = CIDR + CIDR_dict[num_of_subnets]
    octet = 4
    if new_CIDR > 30:
        print("Yo, that won't work.")
        return
    net_ID = network_ID
    list_of_net_IDs.append(net_ID)
    new_block_size = 2 ** (32 - new_CIDR)
    while new_block_size > 256:  # and octet not <= 1?
        octet -= 1
        new_block_size = new_block_size // 256
        print("Block:", new_block_size, "Octet", octet)
    for i in range(num_of_subnets):
        # if network_ID not in list_of_net_IDs:
        # list_of_net_IDs.append(network_ID)
        net_ID = list_of_net_IDs[i][:]
        #print(list_of_net_IDs, list_of_net_IDs[i])
        net_ID[octet - 1] += new_block_size #111.254.128.0
        if net_ID[octet - 1] > 255:  #111.255.256.0
            net_ID[octet - 2] += 1   #111.256.256.0
            net_ID[octet - 1] -= 256 #111.256.0.0
            if net_ID[octet - 2] > 255:
                net_ID[octet - 3] += 1 #112.256.0.0
                net_ID[octet - 2] -= 256 #112.0.0.0
                if net_ID[octet - 3] > 255:
                    net_ID[octet - 4] += 1
                    net_ID[octet - 3] -= 256
        #new_net_ID = net_ID[:]
        list_of_net_IDs.append(net_ID[:])

def subnet_first_IPs(list_of_net_IDs):
    count = len(list_of_net_IDs)
    for i in range(0, count):
        net_ID = list_of_net_IDs[i][:]

        net_ID[3] += 1
        if net_ID[3] > 255:
            net_ID[2] += 1
            net_ID[3] -= 256
            if net_ID[2] > 255:
                net_ID[1] += 1
                net_ID[2] -= 256
                if net_ID[1] > 255:
                    net_ID[1] += 1
        list_of_first_IPs.append(net_ID)


# Idea: Send the list from above, redo the BC determination, save it on the new list, repeat for length of list
def subnet_bc_IPs(list_of_net_IDs):
    count = len(list_of_net_IDs)
    for i in range(0, count):
        bcNetz = list_of_net_IDs[i][:]

        bcNetz[3] -= 1

        if bcNetz[3] == 0 or bcNetz[3] == -1:
            bcNetz[3] = 255
            bcNetz[2] -= 1
            if bcNetz[2] == 0 or bcNetz[2] == -1:
                bcNetz[2] = 255
                bcNetz[1] -= 1
                if bcNetz[1] == 0 or bcNetz[1] == -1:
                    bcNetz[1] = 255
                    bcNetz[0] -= 1
        list_of_bc_IPs.append(bcNetz)

def subnet_last_IPs(list_of_bc_IPs):
    count = len(list_of_bc_IPs)
    for i in range(0, count):
        bcNetz = list_of_bc_IPs[i][:]
        bcNetz[3] -= 1

        if bcNetz[3] == 0 or bcNetz[3] == -1:
            bcNetz[3] = 255
            bcNetz[2] -= 1
            if bcNetz[2] == 0 or bcNetz[2] == -1:
                bcNetz[2] = 255
                bcNetz[1] -= 1
                if bcNetz[1] == 0 or bcNetz[1] == -1:
                    bcNetz[1] = 255
                    bcNetz[0] -=1
        list_of_last_IPs.append(bcNetz)


subnet_net_IDs(network_ID, CIDR, num_of_subnets)


subnet_first_IPs(list_of_net_IDs)



subnet_bc_IPs(list_of_net_IDs)

list_of_bc_IPs=list_of_bc_IPs[1:]
subnet_last_IPs(list_of_bc_IPs)


list_of_net_IDs=list_of_net_IDs[:-1]
list_of_first_IPs=list_of_first_IPs[:-1]

#list_of_last_IPs=list_of_last_IPs[:]

print("Net-IDs", list_of_net_IDs)
print("First IPs", list_of_first_IPs)
print("Last IPs", list_of_last_IPs)
print("Broadcasts", list_of_bc_IPs)
print()
print("  Start Address  |   End Address  |  Network Address  |  Broadcast Address ")
for i in range(len(list_of_net_IDs)):

    print(list_of_first_IPs[i], "|", list_of_last_IPs[i], "|", list_of_net_IDs[i], "|", list_of_bc_IPs[i])

