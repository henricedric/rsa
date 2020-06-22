from math import gcd
from random import randrange, getrandbits



a = 'ê b bonjour @ Ù ñ ~~ ^ 6 4 <?? jkfsd a toi à ç £ #&  &  '
# a='une phrase normale 123 45 6'

print(a)

b_1= a.encode(encoding='UTF-8')
b = int.from_bytes(b_1, byteorder="big")

print(b)

c = b_1.decode()

print(c)

def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

def int_to_bytes(value, length):
    result = []

    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)

    result.reverse()

    return result


def is_prime(n, k=128):

    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

#return a probable prime number of a given bits length
def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

#generate_prime_number of a given bits length
def generate_prime_number(length=1024):
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


# help to set up variable
# generate adequate prime number for our p and q
#return p , q and fi n
def find_p_q(e):
    while True:
        p = generate_prime_number()
        q = generate_prime_number()
        fi_n = (p-1)*(q-1)
        if (fi_n>e):
            if (gcd(fi_n,e)==1):
                return p , q, fi_n

#return the multiplicative inverse of two given number
def multiplicative_inverse(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa
    return lx

#encrypt a given message RAS encryption
def encryp_rsa(m,e,n):
    return pow(m,e,n)

#decrypt a given message RAS decryption
def decrypt_rsa(c,d,n):
    return pow(c,d,n)


def chinese_reminder_theorem(c,p,q,e):
    power_p = multiplicative_inverse(e, p-1)%(p-1)
    power_q = multiplicative_inverse(e, q-1)%(q-1)
    mod = multiplicative_inverse(q, p)%(p)


    m1 = pow(c, power_p, p)
    m2 = pow(c, power_q, q)
    h = mod*(m1 - m2) % p

    return m2 + h* q

m= b
# m = 4669218834573094669218834573094669218834573094669218834573094669218834573094669218834573094669218834573093247634267849874328989438793247893214897238972387932879423423874387234897234879348974234287923478932478934278948812347832987948723
e = 65537
p= 0
q=0

p,q , fi_n= find_p_q(e)
n= p*q
d= multiplicative_inverse(e,fi_n)

print('Our private key d = : ',d)
#encrypt

c= encryp_rsa(m, e, n)
print('Our encrypted message C = : ', c)

print('\n------------\n')
print('CRT decryption')
crt=False

m_d_crt= chinese_reminder_theorem(c,p,q,e)


if(m_d_crt == m):
    crt=True
    print('CRT decryption success !')
    print(m_d_crt)
else:
    print('CRT decryption Fail !')


b_2 = m_d_crt.to_bytes(((m_d_crt.bit_length() + 7) // 8), byteorder="big")
m2 = b_2.decode("utf-8")

print(m2)
