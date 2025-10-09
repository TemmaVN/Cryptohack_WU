#!/usr/bin/env python3

from os import urandom
from pwn import *

def bytes_to_word(b):
	return [int.from_bytes(b[i:i+4],'little') for i in range(0,len(b),4)]

def rotate(x, n):
	return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def word(x):
	return x % (2 ** 32)

def words_to_bytes(w):
	return b''.join([i.to_bytes(4, 'little') for i in w])

print(f'{bytes_to_word(b'Hello') = }')
print(f'{words_to_bytes([1819043144, 111]) = }')

def xor(a,b):
	return b''.join([bytes([x^y]) for x,y in zip(a,b)])


def un_rotate(x,n):
	return ((x >> n) & 0xffffffff | ((x << (32 - n)) & 0xffffffff))

print(f'{rotate(112,4) = }')
print(f'{un_rotate(1792,4) = }')



