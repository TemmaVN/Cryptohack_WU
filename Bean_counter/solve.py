#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import AES
import requests

def get_enc():
	url = 'https://aes.cryptohack.org/bean_counter/encrypt/'
	r = requests.get(url)
	return r.json()['encrypted']

ciphertext = get_enc()
print(f'{ciphertext = }')
png_hdr = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52])
c_bytes = bytes.fromhex(ciphertext)

keystream = []

for i in range(len(png_hdr)):
	keystream.append(png_hdr[i] ^ c_bytes[i])

plaintext = [0]*len(c_bytes)
for i in range(len(c_bytes)):
	plaintext[i] = c_bytes[i] ^ keystream[i% len(keystream)]

plaintext = bytes(plaintext)
print(f'{plaintext = }')

with open('flag.png','wb') as fw:
	fw.write(plaintext)