#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad

FLAG = 'crypto{dfbdfsbdjfbjdsfl}'
KEY = os.urandom(16)

def check_admin(c_text,iv):
	cipher = AES.new(KEY,AES.MODE_CBC,iv)
	tst = bytes.fromhex(c_text)
	check = cipher.decrypt(tst).decode()
	print(f'{check = }')
	print(f'{len(check) = }')
	if 'admin=True' in check:
		print(f'{FLAG = }')
		exit()
	else:
		print('{error : you are not the admin}')

def get_cookie():
	text = 'admin=False:Not_for_you_to_break_this'
	print(f'{len(text) = }')
	text_tt = pad(text.encode(),16)
	iv = os.urandom(16)
	cipher = AES.new(KEY,AES.MODE_CBC,iv)
	c_text = cipher.encrypt(text_tt)
	payload = (iv + c_text).hex()
	return {'ciphertext': payload}

cookie = get_cookie()['ciphertext']
iv_old = bytes.fromhex(cookie[0:32])
ciphertext = bytes.fromhex(cookie[32:])

iv_new = xor(b'admin=False',b'admin=True_')
iv_new = xor(iv_old,iv_new)

check_admin(ciphertext.hex(),iv_new)


