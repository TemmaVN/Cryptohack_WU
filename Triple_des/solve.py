#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import DES3 
import requests
import string

def encrypt(key,plaintext):
	url = 'https://aes.cryptohack.org/triple_des/encrypt/'
	r = requests.get(url + key + '/' + plaintext + '/')
	return r.json()['ciphertext']

def encrypt_flag(key):
	url = 'https://aes.cryptohack.org/triple_des/encrypt_flag/'
	r = requests.get(url + key + '/')
	return r.json()

key_solve = b'\x00'*8 + b'\xff'*8
cipher_text = encrypt_flag(key_solve.hex())['ciphertext']
cipher = bytes.fromhex(encrypt(key_solve.hex(),cipher_text))
print(f'{cipher = }')
