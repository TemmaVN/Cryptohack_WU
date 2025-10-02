#!/usr/bin/env python3

from pwn import *
from Crypto.PublicKey import RSA

def read_pem_file(file_path):
	try:
		with open(file_path,'rb') as f:
			pem_data = f.read()
		key = RSA.importKey(pem_data)
		return key 
	except Exception as e:
		print("Can not open file .pem")
		return None

file_path = "/home/temma/Documents/Cryptohack/privacy_enhanced_mail/privacy_enhanced_mail.pem"
key_data = read_pem_file(file_path)
print(f'{key_data.d = }')