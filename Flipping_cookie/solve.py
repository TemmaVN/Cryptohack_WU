#!/usr/bin/env python3

from pwn import *
import requests
from Crypto.Cipher import AES
from datetime import datetime, timedelta

def get_cookie():
	url = "https://aes.cryptohack.org/flipping_cookie/get_cookie/"
	r = requests.get(url)
	return r.json()["cookie"]

cookie = get_cookie()
iv = bytes.fromhex(cookie[0:32])
cipher = bytes.fromhex(cookie[32:])

def check_admin(cookie,iv):
	url = "https://aes.cryptohack.org/flipping_cookie/check_admin/"
	r = requests.get(url + cookie + '/' + iv + '/')
	return r.json()

# print(f'{iv = }')
# admin=Fa --> admin=Tr
# lse;expi --> ue ;expi
#{"cookie":"a02771a208a01811da5bfffd8369669bde0c9e2925f62cc05e28022eef564d28134bf8ce86df7f0ebcf1ba000735cddb"}


expires_at  = (datetime.today() + timedelta(days = 1)).strftime("%s")
real = f'\x00\x00\x00\x00\x00\x00False;expiry='+expires_at
fake = f'\x00\x00\x00\x00\x00\x00True;expiry='+expires_at


xor_time = xor(real.encode(),fake.encode())[0:16]
print(iv.hex())
print(cipher.hex())
print(f'{xor_time.hex() = }')
iv_new = xor(iv,xor_time)
print(iv_new.hex())
print(f'{check_admin(cipher.hex(),iv_new.hex()) = }')