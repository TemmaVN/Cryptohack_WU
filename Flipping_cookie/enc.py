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

def flip(cookie, plain):
    start = plain.find(b'admin=False')
    cookie = bytes.fromhex(cookie)
    iv = [0xff]*16
    cipher_fake = list(cookie)
    fake = b';admin=True;'
    for i in range(len(fake)):
       cipher_fake[16+i] = plain[16+i] ^ cookie[16+i] ^ fake[i]
       iv[start+i] = plain[start+i] ^ cookie[start+i] ^ fake[i]

    cipher_fake = bytes(cipher_fake).hex()
    iv = bytes(iv).hex()
    return cipher_fake, iv

expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
plain = f"admin=False;expiry={expires_at}".encode()
cookie, iv = flip(cookie, plain)
print(f'{iv = }')
