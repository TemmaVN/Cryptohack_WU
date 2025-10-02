#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import AES
import requests
import time 
import string 


def encrypt(payload):
	url = "http://aes.cryptohack.org/ecb_oracle/encrypt/"
	r = requests.get(url+payload+'/')
	return r.json()['ciphertext']

def Print_blk(hex_blk,sz):
	for i in range(0, len(hex_blk), sz):
		print(hex_blk[i:i+sz],' ',end = '')
	print()

def brute_force():
	flag = 'crypto{'
	total = 31
	alphabet = '_' + '@' + '}' + string.digits + string.ascii_lowercase + string.ascii_uppercase
	while True:
		payload = '1'*(total - len(flag))		
		expected = encrypt(payload.encode().hex())
		print('E','',end='')
		Print_blk(expected,32)
		for c in alphabet:
			res = encrypt(bytes.hex((payload + flag + c).encode()))
			print(c,'',end='')
			Print_blk(res,32)
			if res[32:64] == expected[32:64]:
				flag += c 
				print(flag)
				break
			time.sleep(1)

		if flag.endswith('}'): break

	print(flag)

brute_force()