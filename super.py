# List version
def superinput(num, type="string"):
    if num % 1 != 0 or num < 0 or isinstance(num, str):
        print("Amount of inputs entered incorrectly.")
        return
    if type not in ("int", "float", "string"):
        print("Type not specified. Only ""int"", ""float"" or ""string"" are accepted.")
        return
    answer = []
    if type == "int":
        for i in range(0, num):
            while True:
                inp = input(f"Int {i+1} of {num}? ")
                try:
                    inp = int(inp)
                except ValueError:
                    print("Input not an integer. Please try again.")
                if isinstance(inp, int):
                    break
            answer.append(inp)
    if type == "float":
        for i in range(0, num):
            while True:
                inp = input(f"Float {i + 1} of {num}? ")
                try:
                    inp = float(inp)
                except ValueError:
                    print("Input not a float. Please try again.")
                if isinstance(inp, float):
                    break
            answer.append(inp)
    if type == "string":
        for i in range(0, num):
            inp = input(f"String {i + 1} of {num}? ")
            answer.append(inp)
    return answer

"""
answer = superinput(4, "float")
input_1, input_2, input_3, input_4 = answer
print(input_1, input_2, input_3, input_4)
"""

def super(num, type="string"):
    print(f"This function will ask {num} inputs of the {type} type.")
    return superinput(num, type)

"""
for i in range(num):
    answer = super(4, "float")
print(answer)
"""

"""
inputs = super(4, "float")


for i in range(len(inputs)):
    print("Input", i+1, "was", inputs[i])

"""

# Dictionary version

"""
def supereingabe2(num, type="string"):
    if num % 1 != 0 or num < 0 or isinstance(num, str):
        print("Amount of inputs entered incorrectly.")
        return
    if type not in ("int", "float", "string"):
        print("Type not specified. Only ""int"", ""float"" or ""string"" are accepted.")
        return
    answer = {}
    if type == "int":
        for i in range(0, num):
            while True:
                inp = input(f"Int {i+1} of {num}? ")
                try:
                    inp = int(inp)
                except ValueError:
                    print("Input not an integer. Please try again.")
                if isinstance(inp, int):
                    break
            answer["Input"+ str(i+1)] = inp
    if type == "float":
        for i in range(0, num):
            while True:
                inp = input(f"Float {i + 1} of {num}? ")
                try:
                    inp = float(inp)
                except ValueError:
                    print("Input not a float. Please try again.")
                if isinstance(inp, float):
                    break
            answer.append(inp)
    if type == "string":
        for i in range(0, num):
            inp = input(f"String {i + 1} of {num}? ")
            answer.append(inp)
    return answer

answer = supereingabe2(4, "int")
print(answer.values())

"""