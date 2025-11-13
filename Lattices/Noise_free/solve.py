#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import json
from tqdm import tqdm
import ast

io = remote('socket.cryptohack.org',13411)

n_di = 64
# plaintext modulus
p = 257
# ciphertext modulus
q = 0x10001

def send_json(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

io.recvline()
the_row = []
b_full = []
for _ in range(64):
	payload = {'option': 'encrypt', 'message': '0'}
	send_json(payload)
	data = recv_json()
	the_row.append(ast.literal_eval(data["A"]))
	b_full.append(int(data["b"]))


import time
def gauss_elimination_gf(A, b, q):
    """Gaussian elimination over GF(q)"""
    rows, cols = len(A), len(A[0])
    
    # Create augmented matrix
    Ab = [A[i] + [b[i]] for i in range(rows)]
    
    # Forward elimination
    for col in tqdm(range(min(rows, cols))):
        # Find pivot
        pivot_row = None
        for row in range(col, rows):
            if Ab[row][col] % q != 0:
                pivot_row = row
                break
        
        if pivot_row is None:
            continue
        
        # Swap rows
        Ab[col], Ab[pivot_row] = Ab[pivot_row], Ab[col]
        
        # Scale pivot row
        pivot = Ab[col][col] % q
        pivot_inv = inverse(pivot, q)
        if pivot_inv is None:
            continue
            
        for j in range(cols + 1):
            Ab[col][j] = (Ab[col][j] * pivot_inv) % q
        
        # Eliminate column
        for row in range(rows):
            if row != col:
                factor = Ab[row][col] % q
                for j in range(cols + 1):
                    Ab[row][j] = (Ab[row][j] - factor * Ab[col][j]) % q
        print(f'{Ab = }')
        time.sleep(3)
    # Extract solution
    solution = [0] * cols
    for i in range(min(rows, cols)):
        solution[i] = Ab[i][-1] % q
    
    return solution


# def gauss_elimination_gf1(A,b,q):
# 	rows, cols = len(A), len(A[0])
# 	Ab = [A[i] + [b[i]] for i in range(len(A))]
# 	for col in tqdm(range(cols)):
# 		#find pivot 
# 		pivot = None
# 		for row in range(col,rows):
# 			if Ab[row][col] % q != 0: 
# 				pivot = row
# 				break
# 		if pivot is None: continue
# 		Ab[col], Ab[pivot] = Ab[pivot], Ab[col]
# 		#Inv of the pivot
# 		inv_p = inverse(Ab[col][col]%q,q)
# 		if inv_p is None: continue
# 		#eliminate the data
# 		for row in range(rows):
# 			if col == row: continue
# 			factor = (Ab[row][col]*inv_p)%q 
# 			for j in range(cols + 1):
# 				Ab[row][j] = (Ab[row][j] - factor*Ab[col][j])%q 
# 		print(f'{Ab = }')
# 		time.sleep(3)
# 	solution = []
# 	for i in Ab:
# 		solution.append(i[-1])
# 	return solution


# print(gauss_elimination_gf1([[1,1,1,1],[1,1,1,2],[1,1,2,3],[1,2,3,4]],[10,14,21,30],0x10001))



S = gauss_elimination_gf(the_row,b_full,q)
print(S)
idx = 0 
flag = ''
def mul_arr(A,B):
	if len(A) != len(B): return -1
	res = 0
	for i in range(len(A)):
		res = (res+A[i]*B[i])%q
	return res 
while True:
	payload = {'option': 'get_flag', 'index' : str(idx)}
	send_json(payload)
	data = recv_json()
	A = ast.literal_eval(data["A"])
	b = int(data["b"])
	newbie = chr(b - mul_arr(A,S))
	flag += newbie
	idx += 1
	if newbie == '}': break

print(f'{flag = }')

io.interactive()
