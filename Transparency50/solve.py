#!/usr/bin/env python3

from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes 

def open_pem_file(file_path):
	try:
		with open(file_path,'rb') as f:
			data = f.read()
		key = RSA.importKey(data)
		return key 
	except Exception as e:
		print(f'error {e}')
		return None 

file_path = 'transparency.pem'
key = open_pem_file(file_path)
e = key.e 
print(f'{e = }')
n = key.n
print(f'{n = }')
print(f'{long_to_bytes(n) = }')
