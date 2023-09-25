def max2(*values):
    values = list(values)
    if len(values) == 1:
        return values[0]
    if values[0] >= values[1]:
        values.remove(values[1])
    else:
        values.remove(values[0])
    return max2(*values)

nums = 1,3,5
print(max2(1,3,5))

print(max2(*nums))

b = []
while True:
    a = input("Numbers? Enter [a] to abort: ")
    if a == "a":
        break
    else:
        b.append(a)
b = [int(x) for x in b]
print(b)

if len(b) > 1:
    print(max2(*b))
else:
    print(max2(b))


"""
def min2(*values):
    values = list(values)
    if len(values) == 1:
        return values[0]
    if values[0] <= values[1]:
        values.remove(values[1])
    else:
        values.remove(values[0])
    return min2(*values)

print(min2(1,3,5))
"""
