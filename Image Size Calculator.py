unitDict = {"B":1, "KB": 1/1000, "MB": 1/(1000**2), "GB": 1/(1000**3), "KiB": 1/1024, "MiB": 1/(1024**2), "GiB": 1/(1024**3)}
unitBinary = ["B", "KiB", "MiB", "GiB"]
unitDecimal = ["B", "KB", "MB", "GB"]
binary, decimal = False, False
r1, r2 = 0, 0
height, width, bitrate, compression = "","","",""
# Asking for user inputs
while True:
    while True:
        height = input("Height of the image in pixels: ")
        # Making sure we get a float we can work with.
        try:
            height = float(height)
        except ValueError:
            print("Input not recognized.")
        if type(height) == float:
            break
    while True:
        width = input("Width of the image in pixels: ")
        try:
            width = float(width)
        except ValueError:
            print("Input not recognized.")
        if type(width) == float:
            break
    while True:
        bitrate = input("Bitrate: ")
        try:
            bitrate = float(bitrate)
        except ValueError:
            print("Input not recognized.")
        if type(bitrate) == float:
            break
    while True:
        compression = input("Compression in %: ")
        try:
            compression = float(compression)
        except ValueError:
            print("Input not recognized.")
        if type(compression) == float:
            if compression < 100:
                break
            print("Compression exceeds 100%.")
    compression = (100-compression)/100
    # Check if entered unit is part of the dictionary. If not, ask again (it's a loop).
    while True:
        unit = input("Convert into which unit? [B, KB, MB, GB; B, KiB, MiB, GiB] ")
        if unit in unitDict:
            break
        print("Unit not recognized. The input is case sensitive.")
    # We check which unit was entered for a later conversion. Since "B" is in both, we have to exclude it.
    if unit != "B":
        if unit in unitBinary:
            binary = True
            unit_index_b = unitBinary.index(unit)
        if unit in unitDecimal:
            decimal = True
            unit_index_d = unitDecimal.index(unit)
    # Calculation
    result = (height * width * bitrate * compression * unitDict[unit])/8
    print("Your image size is {0:.4f} {1}.".format(result, unit))
    # Normally we'd be done. But if the number is too low, it's useless. So we have to convert it to the smaller unit.
    r1 = result # Save the original result to compare with r2 (result after conversion) later. If r2 == r1 we don't want to print the same thing twice.
    # Conversion happens here. We check whether it is binary or decimal (important for multiplicator), then adjust the unit in a loop.
    while result < 0.01 and unit != "B" and binary:
        result = result * 1024
        unit = unitBinary[unit_index_b-1]
        r2 = result
    while result < 0.01 and unit != "B" and decimal:
        result = result * 1000
        unit = unitDecimal[unit_index_d-1]
        r2 = result
    if r2 > r1:
        print("Your image size was very small for the given unit. This might be more readable: {0:.4f} {1}.".format(result, unit))
    # Ask if we want to run the program again.
    while True:
        rerun_check = input("Run again? [y/n] ")
        if rerun_check in ("y", "n"):
            break
        print("Invalid input.")
    if rerun_check == "y":
        continue
    else:
        print("Goodbye!")
        break

