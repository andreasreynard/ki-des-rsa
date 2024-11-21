def public_key(owner):
    if owner == 1:
        prime1, prime2, e = 101, 257, 2327
    elif owner == 2:
        prime1, prime2, e = 193, 241, 10001
    return [e, prime1 * prime2]
