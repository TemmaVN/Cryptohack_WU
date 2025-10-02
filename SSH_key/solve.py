#!/usr/bin/env python3

from pwn import *
from Crypto.PublicKey import RSA
import paramiko

def open_pem_file(file_path):
	try:
		with open(file_path,'rb') as f:
			data = f.read()
		key = RSA.importKey(data)
		return key 
	except Exception as e: 
		print("Can open .pem file ")
		return None

file_path = '/home/temma/Documents/Cryptohack/SSH_key/bruce_rsa.pem'
key = open_pem_file(file_path)
print(f'{key.n = }')

def open_pub_file(file_path):
	try:
		ssh_key = paramiko.PKey.from_path(file_path)
		if not isinstance(ssh_key, paramiko.RSAKey):
			raise ValueError("File does not contain an RSA key")
		# get n and e
		n = ssh_key.get_n()
		e = ssh_key.get_e()
		key = RSA.construct((n,e))
		return key
	except Exception as e:
		print(f"Error {e}")
		return None

file_path = '/home/temma/Documents/Cryptohack/SSH_key/bruce_rsa.pub'
key = open_pub_file(file_path)
print(f'{key = }')
