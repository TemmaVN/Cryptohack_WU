#!/usr/bin/env python3

from decimal import *
from fpylll import IntegerMatrix, LLL, GSO, BKZ
from math import floor

getcontext().prec = 100
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433
length = 23
M = IntegerMatrix(length + 1, length + 1)
for i in range(length):
	for j in range(length):
		if i == j: M[i,j] = 1 
		else: M[i,j] =0 

for i in range(length):
	M[i,length] = floor(Decimal(PRIMES[i]).sqrt()*16**64)
M[length,length] = ct 
param = BKZ.Param(block_size = length + 1)
BKZ.reduction(M, param)
flag = ''
for i in range(length):
	flag += chr(abs(M[0][i]) )
	print(f'{abs(M[0][i]) = }')
print(f'{flag = }')