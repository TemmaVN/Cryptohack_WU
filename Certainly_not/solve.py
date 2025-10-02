#!/usr/bin/env python3

from pwn import *
from Crypto.PublicKey import RSA

def read_der_file(file_path):
	try:
		with open(file_path,'rb') as f:
			der_data = f.read()
		key = RSA.importKey(der_data)
		return key 
	except Exception as e:
		print('Can not open the file')
		return None

file_path = '/home/temma/Documents/Cryptohack/Certainly_not/2048b_rsa_example_cert.der'
key = read_der_file(file_path)
print(f'{key.n = }')