#!/usr/bin/env python3

a = []
b = []
c = []
d = []
root = []

from hashlib import sha256
from Crypto.Util.number import long_to_bytes
import os
import ast

def hash256(data):
    return sha256(data).digest()

def merge_nodes(a, b):
    return hash256(a+b)

with open('output.txt','r') as f:
	for line in f:
		data = ast.literal_eval(line)
		print(f'{line = }')
		a.append(bytes.fromhex(data[0]))
		b.append(bytes.fromhex(data[1]))
		c.append(bytes.fromhex(data[2]))
		d.append(bytes.fromhex(data[3]))
		root.append(bytes.fromhex(data[4]))

bin_data = ''
for i in range(len(root)):
	left = merge_nodes(a[i],b[i])
	right = merge_nodes(c[i],d[i])
	root_tst = merge_nodes(left, right)
	if root_tst == root[i]: bin_data += '1'
	else: bin_data += '0'

print(f'{long_to_bytes(int(bin_data,2)) = }')