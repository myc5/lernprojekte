"""
Step 1: Min(List)
Step 2: Add min(List) to empty List
Step 3: Remove min(list) from original List
Step 4: Repeat until original List is empty or has one value
Step 5: print formerly empty list, it is now sorted
"""

Liste = [7, 3, 2, 5, 2]
Liste2 = []

"""This works but let's try it via functions
while len(Liste) > 1:
    moo = min(Liste)
    Liste2.append(moo)
    Liste.remove(moo)
Liste2.append(Liste[0])

print(Liste2)
"""

def min2(*args):
    arglist = list(args)
    if len(arglist) == 1:
        return arglist
    if arglist[0] >= arglist[1]:
        return min2(*arglist[1:])
    else:
        arglist.remove(arglist[1])
        return min2(*arglist)

def max2(*args):
    arglist = list(args)
    if len(arglist) == 1:
        return arglist
    if arglist[0] <= arglist[1]:
        return max2(*arglist[1:])
    else:
        arglist.remove(arglist[1])
        return max2(*arglist)

def sort_asc(*args):
    sortedList = []
    try:
        arglist = list(*args)
    except TypeError:
        arglist = list(args)
    while len(arglist) > 0:
        smallest = min2(*arglist)
        sortedList.append(smallest[0])
        arglist.remove(smallest[0])
    return sortedList

def sort_desc(*args):
    sortedList = []
    try:
        arglist = list(*args)
    except TypeError:
        arglist = list(args)
    while len(arglist) > 0:
        biggest = max2(*arglist)
        sortedList.append(biggest[0])
        arglist.remove(biggest[0])
    return sortedList

print("Original-Liste:", Liste)
print("Liste, aufsteigend sortiert:", sort_asc(Liste))
print("Liste, absteigend sortiert:", sort_desc(Liste))
print(sort_asc(2, 5, 1, 2, 8, 9))
print(sort_desc(2, 2, 1, 5, 7, 5))

