#!/usr/bin/env python3

from Crypto.Util.number import *
from collections import namedtuple

# E:Y**2=X**3+486662*X**2+X mod(2**255−19)
b = 1
a = 486662
p = 2**255 - 19
Point = namedtuple('Point','x y')

def Tonelli_shanks(n,p):
	assert pow(n,(p-1)//2,p) == 1
	# p - 1 = q * 2 ** s
	q = p -1 
	while not q&1:
		q>>=1
		s+=1
	