#!/usr/bin/env python3

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import time
from Crypto.Util.number import *

for i in range(1,50):
	print(f'{i = }')
	file_path = str(i) + '.pem'
	with open(file_path,'rb') as f:
		key = RSA.importKey(f.read())
	print(f'{key = }')

