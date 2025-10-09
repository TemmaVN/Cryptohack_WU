#!/usr/bin/env python3

from pwn import *
import json 

io = remote('socket.cryptohack.org',13399)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

def send_json(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

idx = 1
while 1:
	io.recvline()
	send_json({'option': 'reset_password','token':(b'\x00'*28).hex()})
	send_json({'option': 'authenticate','password':''})
	io.recvline()
	check = io.recvline().decode().rstrip()
	if 'crypto' in check:
		print(f'{check = }')
		break
	send_json({'option': 'reset_connection'})
	if idx%100 == 0:print(f'{idx = }')
	idx+=1

io.interactive()

# from pwn import *
# import json

# t = (b"\x00" * 28).hex()
# data = {"option": "reset_password", "token": t}
# r = connect('socket.cryptohack.org' ,13399)
# r.recvline()
# json_data = json.dumps(data).encode()
# idx = 0

# while 1:
#     r.sendline(json_data)
#     r.recvline()
#     p = {"option": "authenticate", "password": ""}
#     json_password = json.dumps(p).encode()
#     r.sendline(json_password)
#     out = (r.recvline()).decode()
#     if "crypto" in out:
#         print(out)
#         break
#     reset = {"option": "reset_connection"}
#     json_reset = json.dumps(reset).encode()
#     r.sendline(json_reset)
#     r.recvline()
#     if idx%100 == 0:
#     	print(f'{idx = }')
#     idx +=1