def norm_gcd(a, b):
    if b == 0:
        return a
    return norm_gcd(b, a % b)

if __name__ == '__main__':
    n1 = int(input("1st number: "))
    n2 = int(input("2nd number: "))
    print(norm_gcd(n1, n2))
