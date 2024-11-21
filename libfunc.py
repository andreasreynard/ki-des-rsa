def phi(n):
    if n % 2 == 0:
        return n // 2 - 1
    if n % 3 == 0:
        return 2 * n // 3 - 2
    i = 5
    while i * i <= n:
        if n % i == 0:
            return (i - 1) * (n // i - 1)
        i += 2
        if n % i == 0:
            return (i - 1) * (n // i - 1)
        i += 4
    
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

def encoder(message, key):
    enc_message = []
    for letter in message:
        enc_message.append(des(ord(letter), key))
    return enc_message

def decoder(message, key):
    dec_message = ''
    for num in message:
        dec_message += chr(des(num, key))
    return dec_message

def des(base, pm):
    power, mod = pm[0], pm[1]
    if power == 0:
        return 1
    res = des(base, [power // 2, mod])
    res = (res * res) % mod
    if power % 2 == 1:
        res = (res * base) % mod
    return res
