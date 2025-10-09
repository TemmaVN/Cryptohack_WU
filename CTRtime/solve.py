#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import AES
import requests
import string
import time

def encrypt(plaintext):
	url = 'https://aes.cryptohack.org/ctrime/encrypt/'
	r = requests.get(url + plaintext + '/')
	return r.json()['ciphertext']

alphabelt =	'@' + '!' + '{' + '}' + '_' + string.digits + string.ascii_lowercase + string.ascii_uppercase + '?'

flag = 'crypto{CRIME'
len_check = len(encrypt(flag.encode().hex()))
idx = 0
while idx < 66:
	for i in alphabelt:
		len_test = len(encrypt((flag + i).encode().hex()))
		if len_check == len_test:
			flag += i 
			break 
	if flag.endswith('}'):
		print(f'{flag = }')
		break 
	idx +=1
	print(f'{flag = }')

if idx == 66: print("Can not find flag")