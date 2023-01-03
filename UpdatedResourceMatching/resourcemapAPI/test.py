def f(a):
    if a==0:
        return 1
    return a*f(a-1)
f2 = lambda a,b: abs(2 * a - 3 * b)
print(f(f2(2,3)))