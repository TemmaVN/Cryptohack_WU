#!/usr/bin/env python3

from pwn import *
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def encrypt(data):
	if len(data) % 32 != 0: return None
	url = 'https://aes.cryptohack.org/lazy_cbc/encrypt/'
	r = requests.get(url + data + '/')
	return r.json()['ciphertext']

def decrypt(data):
	if len(data) % 32 != 0: return None 
	url = 'https://aes.cryptohack.org/lazy_cbc/receive/'
	r = requests.get(url + data + '/')
	return r.json()

def check_key(key):
	if len(key) != 32: return None
	url = 'https://aes.cryptohack.org/lazy_cbc/get_flag/'
	r = requests.get(url + key + '/')
	return r.json()

c0 = c2 = os.urandom(16)
c1 =  b'\x00'*16
plain = decrypt((c0 + c1 + c2).hex())['error']
plain = plain.replace('Invalid plaintext: ','')
p0 = bytes.fromhex(plain[0:32])
p2 = bytes.fromhex(plain[64:])
print(f'{len(p0) = }')
print(f'{len(p2) = }')
iv = xor(p0,p2)
flag = bytes.fromhex(check_key(iv.hex())['plaintext'])
print(f'{flag = }')

