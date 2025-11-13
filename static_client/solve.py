#!/usr/bin/env python3

from pwn import *
import json

io = remote('socket.cryptohack.org',13373)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

def send_json(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

io.recvuntil(b'Intercepted from Alice:')
Alice_Intercepted = recv_json()
io.recvuntil(b'Intercepted from Bob:')
Bob_Intercepted = recv_json()
io.recvuntil(b'Intercepted from Alice:')
Alice_enc = recv_json()
print(f'{Alice_Intercepted = }')
print(f'{Bob_Intercepted = }')
print(f'{Alice_enc = }')
payload = {'p': Alice_Intercepted['p'], 'g': Alice_Intercepted['A'], 'A':'0x01'}

send_json(payload)
io.recvuntil(b'Bob says to you: ')
Bob_new = recv_json()['B']
io.recvuntil(b'Bob says to you: ')
data = recv_json()
iv = Alice_enc['iv']
enc = Alice_enc['encrypted']
print(f'{Bob_new = }')
print(f'{iv = }')
print(f'{enc = }')
from decrypt import decrypt_flag
flag = decrypt_flag(int(Bob_new,16),iv,enc)
print(f'{flag = }')
io.interactive()