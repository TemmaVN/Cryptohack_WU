#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import json

io = remote('socket.cryptohack.org',13403)

def json_recv():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

def json_send(data):
	payload = json.dumps(data)
	io.sendline(payload.encode())

io.recvuntil(b'Prime generated: ')
q = int(io.recvline().decode().replace('"','').rstrip()[2:],16)
print(f'{q = }')
io.recvuntil(b'pow(g,q,n) = 1:')

#=====================find g and n================================#
g = q +1
n = q**2
payload = {'g':hex(g),'n':hex(n)}
json_send(payload)
io.recvuntil(b'public key: ')
h = int(io.recvline().decode().replace('"','').rstrip()[2:],16)
x = (h-1)//q
payload = {'x': hex(x)}
json_send(payload)
io.interactive()
