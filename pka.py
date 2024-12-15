from datetime import datetime
import secrets

def gen_keys(owner):
    if owner == 1:
        p, q, e = 101, 257, 2327
    elif owner == 2:
        p, q, e = 193, 241, 10001
    n = p * q
    phi = (p - 1) * (q - 1)
    d = mod_inv(e, phi)
    return (e, n), (d, n)

def mod_inv(a, m):
    gcd, x, _ = ext_gcd(a, m)
    return x % m

def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = ext_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def verified():
    return "OK, the request's verified!"

def better_pow(base, pm):
    power, mod = pm[0], pm[1]
    if power == 0:
        return 1
    res = better_pow(base, [power // 2, mod])
    res = (res * res) % mod
    if power % 2 == 1:
        res = (res * base) % mod
    return res
