#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import json

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

for i in range(100):
	print(f'{generate_basis(i) = }')