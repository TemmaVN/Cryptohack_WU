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
request = {
	'document': ['0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4', 'c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef']
}
send_recv(request)
io.interactive()