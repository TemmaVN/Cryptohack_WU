#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def get_key():
	try:
		with open('key.pem','rb') as f:
			data = f.read()
		key = RSA.importKey(data)
		return key 
	except Exception as e:
		print(e)

a = get_key()
n = a.n 
e = a.e 
c = 0x249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28
