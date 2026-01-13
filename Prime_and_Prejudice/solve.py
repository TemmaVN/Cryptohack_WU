#!/usr/bin/env python3

from Crypto.Util.number import *
import itertools
from tqdm import tqdm

def generate_basic(n):
    basic = [True]*n 
    for i in range(3,int(n**0.5)+1,2):
        if basic[i]:
            basic[i*i::2*i] = [False]*((n - i*i - 1)//(2*i) + 1)
    return [2] + [i for i in range(3,n,2) if basic[i]]

def miller_rabin(n,b):
    if n == 2 or n == 3: return True
    if n<=1 or n %2 == 0: return False
    r,s = 0, n-1
    while s%2 == 0:
        s >>= 1
        r += 1

    basic = generate_basic(b)
    for b in basic:
        x = pow(b,s,n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = pow(x,2,n)
            if x == n-1:
                break
        else:
            return False
    return True

def xgcd(a,b):
    s = 0
    t = 1 
    r = b  
    s1 = 1 
    t1 = 0 
    r1 = a  
    while not (r == 0):
        q = r1 // r 
        r1, r = r, r1 - q*r 
        s1, s = s, s1 - q*s 
        t1, t = t, t1 - q*t 
    return (r1,s1,t1)

def crt1(residures, modulos):
    rm = list(zip(residures, modulos))
    cur_res , cur_mod = rm[0]
    for r,m in rm[1:]:
        g = GCD(cur_mod, m)
        if not r % g == cur_res %g:
            return -1, -1
        r1,s,t = xgcd(m//g,cur_mod//g)
        cur_res = cur_res * (m//g) * s + r * (cur_mod//g) * t 
        cur_mod *= m//g
        cur_res %= cur_mod
    return cur_res, cur_mod

primes = generate_basic(64)
print(f'{len(primes) = }')
fool = []
h = 3
def legendre(a,p):
    return pow(a,(p-1)//2,p)

for p in primes:
    f = set()
    for i in generate_basic(200*p)[1:]:
        if legendre(p,i) == i-1:
            f.add(i % (4*p))
    fool.append(list(f))

print(fool)
ks = [1, 998244353, 233] 
fool2 = []

for p, f in enumerate(fool):
    prime = primes[p]
    m = prime*4
    cur_set = set(f)
    for i in range(1,h):
        new_set = set()
        for ff in f:
            if ((ff + ks[i] - 1)*inverse(ks[i],m)) % 4 == 3:
                new_set.add(((ff + ks[i] - 1)*inverse(ks[i],m)) % m)
        cur_set = cur_set.intersection(new_set)
    fool2.append(cur_set)

print(f'{fool2 = }')
mm = 1
for a in fool2:
    mm *= len(a)

print(f'{mm = }')
pr = 0 
for tup in itertools.product(*fool2):
    residures = []
    modulos = []
    for i, t in enumerate(tup):
        residures.append(t)
        modulos.append(primes[i]*4)
    residures.append(ks[1] - inverse(ks[2],ks[1]))
    modulos.append(ks[1])
    residures.append(ks[2] - inverse(ks[1], ks[2]))
    modulos.append(ks[2])

    sol, modul = crt1(residures, modulos)
    found = False
    if not sol == -1:
        cur_t = sol
        cur_t = 2**73*modul + cur_t
        for i in tqdm(range(100000)):
            if isPrime(cur_t):
                fin = cur_t
                facs = [cur_t]
                for ii in range(1,h):
                    facs.append(ks[ii]*(cur_t-1) + 1)
                    fin *= ks[ii]*(cur_t - 1) + 1
                if (miller_rabin(fin,64)):
                    print(f'{isPrime(fin) = }')
                    print(f'{fin = }')
                    print(f'{facs = }')
                    if fin.bit_length() >= 600 and fin.bit_length() <= 900:
                        found = True
                        break 
            cur_t += modul

    if found: 
        break   

import json
from pwn import *
io = remote('socket.cryptohack.org',13385)
def send_json(data):
    payload = json.dumps(data).encode()
    io.sendline(payload)


data = {'prime': fin, 'base': facs[0]}
send_json(data)
io.interactive()
