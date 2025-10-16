#!/usr/bin/env python3

from pwn import *
import requests
from Crypto.Cipher import ARC4

def send_cmd(ciphertext, nonce):
	url = 'https://aes.cryptohack.org/oh_snap/send_cmd/'
	r = requests.get(url + ciphertext + '/' + nonce + '/')
	return r.json()

print(f'{send_cmd('a'*100,'63727970746f63727970746f') = }')