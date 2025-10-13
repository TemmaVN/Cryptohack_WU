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

def un_quarter_round(x,a,b,c,d):
	x[b] = un_rotate(x[b],7); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
	x[d] = un_rotate(x[d],8); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
	x[b] = un_rotate(x[b],12); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
	x[d] = un_rotate(x[d],16); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
	return x

def un_inner_block(state):
	state = un_quarter_round(state,3,4,9,14)
	state = un_quarter_round(state,2,7,8,13)
	state = un_quarter_round(state,1,6,11,12)
	state = un_quarter_round(state,0,5,10,15)
	state = un_quarter_round(state,3,7,11,15)
	state = un_quarter_round(state,2,6,10,14)
	state = un_quarter_round(state,1,5,9,13)
	state = un_quarter_round(state,0,4,8,12)
	return state

def get_key(c,m,iv):
	k = b''
	res = []
	iv = bytes.fromhex(iv)
	c = bytes.fromhex(c)
	for i in range(0, len(m), 64):
		res.append(bytes_to_word(xor(m[i:i+64],c[i:i+64])))
	return res 

msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
iv = 'e42758d6d218013ea63e3c49'
c = 'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f'

state = get_key(c,msg,iv)[0]
for i in range(10):
	state = un_inner_block(state)

print(f'{state = }')
idx = 0
for i in state:
	if i == 1: break
	else: idx +=1

key_words = state[4:idx]
key = words_to_bytes(key_words)
print(f'{key = }')
def quarter_round(x, a, b, c, d):
    x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
    x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
    x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
    x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    return x 

def inner_block(state):
    state = quarter_round(state, 0, 4, 8, 12)
    state = quarter_round(state, 1, 5, 9, 13)
    state = quarter_round(state, 2, 6, 10, 14)
    state = quarter_round(state, 3, 7, 11, 15)
    state = quarter_round(state, 0, 5, 10, 15)
    state = quarter_round(state, 1, 6, 11, 12)
    state = quarter_round(state, 2, 7, 8, 13)
    state = quarter_round(state, 3, 4, 9, 14)
    return state

def setup_state(key,iv,counter):
	state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
	state.extend(bytes_to_word(key))
	state.append(counter)
	state.extend(bytes_to_word(iv))
	return state

def decrypt(c, key, iv, counter):
	c = bytes.fromhex(c)
	iv = bytes.fromhex(iv)
	m = b''
	for i in range(0,len(c),64):
		state = setup_state(key,iv,counter)
		for j in range(10):
			state = inner_block(state)
		print(f'{state = }')
		m += xor(c[i:i+64],words_to_bytes(state))
		counter +=1
	return m 

ct = 'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732'
iv2 = 'a99f9a7d097daabd2aa2a235'
print(f'{decrypt(ct,key,iv2,1) = }')
