#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
from gmpy2 import iroot 
from itertools import combinations
from functools import reduce
import operator


n = []
e = []
c = []
idx = 0

with open('output.txt','r') as f:
	for line in f:
		if line != '\n':
			if idx % 3 == 0:
				n.append(int(line.replace('n = ','').rstrip()))
			if idx % 3 == 1:
				e.append(int(line.replace('e = ','').rstrip()))
			if idx % 3 == 2:
				c.append(int(line.replace('c = ','').rstrip()))
			idx += 1

res = []

# def solve(ns, cs):
# 	M = reduce(operator.mul,ns)
# 	Mi = [M // n for n in ns]
# 	ti = [pow(Mr,-1,n) for Mr, n in zip(Mi,ns)]
# 	x = sum([c*t*m for c,t,m in zip(cs,ti,Mi)]) %M
# 	r , exact = iroot(x,3)
# 	if exact:
# 		return r 
# 	else:
# 		return None 

# params = []
# for i, j in zip(n,c):
# 	params.append([i,j])

# for cb in combinations(params,3):
# 	ns = [x[0] for x in cb]
# 	cs = [x[1] for x in cb]
# 	r = solve(ns,cs)
# 	if r == None:
# 		continue
# 	print(f'{long_to_bytes(r).decode() = }')
# for cb in combinations([1,2,3,4,5,6],3):
# 	print(f'{cb = }')

def solve(ns,cs):
	M = reduce(operator.mul,ns)
	Mi = [M // n for n in ns]
	ti = [pow(Mr,-1,n) for Mr, n in zip(Mi,ns)]
	r = sum([m*t*Mr for m,t,Mr in zip(cs,ti,Mi)])%M
	res, is_true = iroot(r,3)
	if is_true:
		return res	
	else:
		return None 

params = []
for i,j in zip(n,c):
	params.append([i,j])

for cb in combinations(params,3):
	ns = [x[0] for x in cb]
	cs = [x[1] for x in cb]
	r = solve(ns,cs)
	if r == None:
		continue
	print(long_to_bytes(r).decode())