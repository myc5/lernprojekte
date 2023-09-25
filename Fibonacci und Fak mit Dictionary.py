def fib(n):
    if n in fibdict:
        return fibdict[n]
    res = fib(n-2) + fib(n-1)
    fibdict[n] = res
    return res

fibdict = {1:1, 2:1, 3:2, 4:3, 5:5, 6:8}
print("Dictionary vorher: ")
print(list(fibdict.values()))
print()
print(f"Fibonacci von 100: {fib(100)}")
print()
print("Dictionary nach Berechnung von fib(100): ")
print(list(fibdict.values()))

def fib2(n):
    if n == 1 or n == 2:
        return 1
    res = fib2(n-2) + fib2(n-1)
    return res

print()
print(f"Fibonacci von 7: {fib2(7)}")

def fac(n):
    if n in facdict:
        return facdict[n]
    res = n * fac(n-1)
    facdict[n] = res
    return res

facdict = {0:1, 1:1, 2:2, 3:6, 4:24, 5:120}

def fac2(n):
    if n == 1 or n == 0:
        return 1
    res = n * fac2(n-1)
    return res

"""x = 20

print(list(facdict.values()))
print(fac(x))
print(list(facdict.values()))
print(fac2(x))"""