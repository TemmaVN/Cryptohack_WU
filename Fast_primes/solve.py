#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import math
import random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long as b2l, inverse, long_to_bytes as l2b
from gmpy2 import is_prime


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
print(f'{n = }')

e = a.e 
c = 0x249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28
M = 166589903787325219380851695350896256250980509594874862046961683989710
p = 51894141255108267693828471848483688186015845988173648228318286999011443419469
q = n//p 
phi = (p-1)*(q-1)
d = inverse(e,phi)
key = RSA.construct((n,e,d))
cipher = PKCS1_OAEP.new(key)
plaintext = cipher.decrypt(l2b(c))
print(f'{plaintext = }')
