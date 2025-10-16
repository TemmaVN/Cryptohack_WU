#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import json
import time

FLAG = 'crypto{????????????????????????????????????}'

# io = remote('socket.cryptohack.org',13385)
# prime = getPrime(800)
# base = prime - 1
# def json_recv():
# 	data = io.recvline().decode().rstrip()
# 	return json.loads(data)

# def json_send(data):
# 	payload = json.dumps(data).encode()
# 	io.sendline(payload)

# payload = {'prime': prime,'base': base}
# json_send(payload)
# io.interactive()

def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        if basis[i]:
            basis[i*i::2*i] = [False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]


def miller_rabin(n, b):
    """
    Miller Rabin test testing over all
    prime basis < b
    """
    basis = generate_basis(b)
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

