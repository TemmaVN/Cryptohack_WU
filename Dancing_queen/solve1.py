#!/usr/bin/env python3

from pwn import *
from os import urandom 

def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def word(x):
    return x % (2 ** 32)

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])

#================================= reverse funtion ==================================#

def un_rotate(x, n):
	return ((x >> n) & 0xffffffff) | ((x << (32 - n)) & 0xffffffff) 

def un_quarter_round(x, a, b, c, d):
	x[b] = un_rotate(x[b], 7); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
	x[d] = un_rotate(x[d], 8); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
	x[b] = un_rotate(x[b], 12); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
	x[d] = un_rotate(x[d], 16); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
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

#def decrypt(enc, iv , key):

#================================= reverse with data ==================================#

iv1 = 'e42758d6d218013ea63e3c49'
iv2 = 'a99f9a7d097daabd2aa2a235'
msg_enc = 'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f'
msg_enc = bytes.fromhex(msg_enc)
msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
flag_enc = 'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732'
state_full = []
counter = 1 
for i in range(0, len(msg_enc), 64):
	tg = xor(msg_enc[i:i+64], msg[i:i+64])
	state = bytes_to_words(tg)
	if len(state) < 16:
		state += [0]*(16 - len(state))
	print(f'{state = }')
	for _ in range(10):
		state = un_inner_block(state) 
	state_full.append(state)
state = state_full[0]
print(f'{state = }')
for i in range(len(state)):
	if state[i] == 1:
		idx = i 
		break

key = words_to_bytes(state[4:idx])
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
def decrypt(enc,key,iv):
	pl = b''
	the_state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
	the_state.extend(bytes_to_words(key))
	the_state.append(1)
	the_state.extend(bytes_to_words(iv))
	for i in range(0,len(enc),64):
		for j in range(10):
			the_state = inner_block(the_state)
		pl += xor(enc[i:i+64],words_to_bytes(the_state))
	return pl

print(f'{decrypt(bytes.fromhex(flag_enc),key,bytes.fromhex(iv2)) = }')


