#!/usr/bin/env python3

from pwn import *
import json

io = remote('socket.cryptohack.org',13405)
def send_recv(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

io.recvline()
send_recv({'document': })
io.interactive()

