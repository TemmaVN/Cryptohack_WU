#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import AES
import requests
import time
import string

alphabet = '_' + '}' + '@' + string.digits + string.ascii_lowercase + string.ascii_uppercase

def encrypt(payload):
	url = "http://aes.cryptohack.org/ecb_oracle/encrypt/"
	r = requests.get(url + payload + '/')
	return r.json()['ciphertext']

def print_block(str,blk_size):
	for i in range(0,len(str),blk_size):
		print(str[i:i+blk_size],'',end='')
	print()

def brute_force():
	flag = ''
	total = 31
	while True:
		payload = '1'*(total - len(flag))
		expected = encrypt(payload.encode().hex())
		print('E','',end='')
		print_block(expected,32)
		for c in alphabet:
			res = encrypt((payload + flag + c).encode().hex())
			print(c,'',end='')
			print_block(res,32)
			if expected[32:64] == res[32:64]:
				flag+=c
				break 
		if flag.endswith('}'): break 
	print(f'{flag = }')

brute_force()