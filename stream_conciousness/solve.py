#!/usr/bin/env python3

from pwn import *
import requests
from Crypto.Cipher import AES
from Crypto.Util import Counter
import time

def get_encrypt():
	url = 'https://aes.cryptohack.org/stream_consciousness/encrypt'
	r = requests.get(url)
	return r.json()['ciphertext']

ciphers = set()
count = len(ciphers)
for _ in range(100):
	ciphers.add(get_encrypt())
	if count < len(ciphers):
		print(f'{count = }')
		print(f'{ciphers = }')
	count = len(ciphers)


def xor_all(ciphers, test_key):
    for cipher in ciphers:
        cipher = bytes.fromhex(cipher)
        for i in range(len(test_key)):
            if i >= len(cipher): break
            a = test_key[i] ^ cipher[i]
            if not (a > 31 and a < 127):
                return False
            print(chr(a), end='')
        print()
        print('cipher', bytes.hex(cipher))
    return True

prefix = b'crypto{'
key = []
encrypted_flag = b''
for c in ciphers:
    c = bytes.fromhex(c)
    k = []
    for i in range(len(prefix)):
        k.append(prefix[i] ^ c[i]) 
    if xor_all(ciphers, k):
        print('found', k, len(k))
        key[:] = k[:]
        encrypted_flag = c
        break

    if key: break


