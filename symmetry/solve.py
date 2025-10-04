#!/usr/bin/env python3

from pwn import *
import requests
from Crypto.Cipher import AES

def encrypt(plaintext,iv):
	if len(iv) != 32: return None
	url = 'https://aes.cryptohack.org/symmetry/encrypt/'
	r = requests.get(url + plaintext + '/' + iv + '/')
	return r.json()['ciphertext']

def encrypt_flag():
	url = 'https://aes.cryptohack.org/symmetry/encrypt_flag/'
	r = requests.get(url)
	return r.json()['ciphertext']

# Get the data of flag
enc = encrypt_flag() 
iv = enc[:32]
cipher_text = enc[32:]
print(f'{iv = }')
print(f'{len(cipher_text) = }')
fake_cipher = b'\x00'*33
full_key_op = encrypt(fake_cipher.hex(),iv)
print(f'{full_key_op = }')
plain = xor(bytes.fromhex(full_key_op),bytes.fromhex(cipher_text))
print(f'{plain = }')

