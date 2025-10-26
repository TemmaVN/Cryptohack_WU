#!/usr/bin/env python3 

from Crypto.Util.number import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import gmpy2
from itertools import combinations

grps = {'n':[], 'e':[], 'c' : []}

for i in range(1,51):
	file_key = str(i) + '.pem'
	file_enc = str(i) + '.ciphertext'
	with open(file_key,'rb') as f:
		key = RSA.importKey(f.read())
	grps['n'].append(key.n)
	grps['e'].append(key.e)
	with open(file_enc,'r') as g:
		c = int(g.read().rstrip(),16)
	grps['c'].append(c)

N = 0
idx = 0
for i in range(len(grps['n'])):
	for j in range(i+1,len(grps['n'])):
		if i == j: continue
		the_gcd = gmpy2.gcd(grps['n'][i],grps['n'][j])
		if the_gcd != 1:
			N = int(the_gcd)
			idx = i 

p = N 
q = grps['n'][idx] // p 
N = p*q 
phi = (p-1)*(q-1)
d = inverse(grps['e'][idx],phi)
key = RSA.construct((N,grps['e'][idx],d))
cipher = PKCS1_OAEP.new(key)
c_bytes = long_to_bytes(grps['c'][idx])
m = cipher.decrypt(c_bytes)
print(f'{m = }')