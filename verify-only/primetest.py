import random

def isProbPrime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(5):
        a = random.randint(2, n - 2)
        x = fastpow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def fastpow(base, power, mod):
    if power == 0:
        return 1
    res = fastpow(base, power // 2, mod)
    res = (res * res) % mod
    if power % 2 == 1:
        res = (res * base) % mod
    return res

num = int(input("Number here: "))
if isProbPrime(num):
    print("Probably Prime")
else:
    print("Composite")
