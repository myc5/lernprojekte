from time import sleep

print("This is a simple app to convert from Base 10 (i.e. 'MB') to Base 2 ('MiB'), or vice versa.")
print("")
print("")

# Added loop to allow the option to rerun.
while True:
    conversion = 0
    unit = 0
    Binary = False
    Decimal = False
    upscale = False
    # Supported units
    B10 = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    B2 = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    # Multipliers, from Bytes
    B10u = [1, 10**3,  10**6, 10**9, 10**12, 10**15, 10**18, 10**21, 10**24]
    B2u = [1, 2**10, 2**20, 2**30, 2**40, 2**50, 2**60, 2**70, 2**80]
    # Experiment with Dictionaries
    DictB10 = {}
    temp_B10u = B10u[:] #Make a copy, don't want to lose the original list.
    for key in B10:
        for value in temp_B10u:
            DictB10[key] = value
            temp_B10u.remove(value) # have to remove the used values so it won't return wrong values
            break # Break is important or it returns wrong values.
    
    DictB2 = {}
    temp_B2u = B2u[:]
    for key in B2:
        for value in temp_B2u:
            DictB2[key] = value
            temp_B2u.remove(value)
        break   
    
    while True:
        choice_unit = input("Enter the unit of the number you want to convert (for example MB, GB, PiB etc): ")
        choice_unit = choice_unit.replace(" ", "") #Remove all spaces, in case user accidentally enters them.
        
        if choice_unit == "B" or choice_unit == "b": # if choice_unit == "B" or "b" was True for things like kB? Why?
            print("We are converting Bytes to... Bytes. Ok then.")
            conversion = 1
            unit = "B"
            break
        
        elif choice_unit in B10:
            print("Converting from Base 10.")
            indexB10 = B10.index(choice_unit) # Check index number of chosen unit, check corresponding number for conversion later.
            conversionB10to2 = B10u[indexB10]/(B2u[indexB10])
            conversion = conversionB10to2
            unit = B2[indexB10]                 # Set opposite unit for print below.
            Binary = True
            break
        
        elif choice_unit in B2:
            print("Converting from Base 2.")
            indexB2 = B2.index(choice_unit) # Like above.
            conversionB2to10 = B2u[indexB2]/(B10u[indexB2])
            conversion = conversionB2to10
            unit = B10[indexB2]
            Decimal = True
            break
        

        print("Invalid input.")
        
    else: 
        print("This really should not have happened...") # This should never get executed
        
    print("")
    print("")
    
    #Check whether a number was entered. If yes, convert to float for conversion. 
    choice_number = input("Enter the whole number itself without units (10, 63, 267.2 etc): ")
    choice_number = choice_number.replace(",", ".") #Convert , to .
    choice_number = choice_number.replace(" ", "") #Remove spaces
    try:
        c_number = float(choice_number)
    except ValueError:
        print("You must enter a number.")
    print("")
    print("")
    print("You chose: " + str(c_number) +" "+ str(choice_unit))

    # Finally time for the result
    result = c_number * conversion
    while result < 0.01 and unit != "B": # This is new: To avoid too small results, convert to next highest unit until the number is bigger or we reach Bytes.
        if Binary:
            result = result * 2**10
            unit = B2[indexB10-1]
            upscale = True
        elif Decimal:
            result = result * 10**3
            unit = B10[indexB2-1]
            upscale = True
    result = round(result, 4) # Conversion was set earlier. Example: if MB was chosen, the conversion divides by 10^6 then  multiplies by 2^20 (both Index 1)   

    print("")
    print("")
    print("DRAMATIC PAUSE"); sleep(0.5)
    print("")
    print("")
    print("Your converted number is: ", result, unit)
    if upscale:
        print("")
        print("(Sorry, but we had to convert to the next lowest unit to make the number human readable.)")
    print("")
    print("")
    
    while True:
        answer = str(input("Run again? (y/n): "))
        if answer in ("y", "n"):
            break
        print("Invalid input.")
    if answer == "y":
        continue
    else:
        print("Sayonara!")
        break


