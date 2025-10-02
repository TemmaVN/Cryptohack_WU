#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import json
import base64

ENCODINGS = [
    "base64",
    "hex",
    "rot13",
    "bigint",
    "utf-8",
]

p = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
	data = p.recvline().decode().rstrip()
	return json.loads(data)

def json_send(data):
	sending = json.dumps(data).encode()
	p.sendline(sending)

def solve_rot_13(c):
	p = ''
	for i in c:
		if (i == '_'): 
			p+= i
			continue
		else:
			tg = ord(i) - ord('a')
			tg = (tg + 13)%26
			p+= chr(tg + ord('a'))
	return p

for _ in range(100):	
	enc = json_recv()
	if (enc["type"] == "base64"): dnc = base64.b64decode(enc["encoded"].encode()).decode()
	elif (enc["type"] == "hex"): dnc = bytes.fromhex(enc["encoded"]).decode()
	elif (enc["type"] == "utf-8"): dnc = "".join(chr(i) for i in enc["encoded"])
	elif (enc["type"] == "bigint"): dnc = long_to_bytes(int(enc["encoded"][2:],16)).decode() 
	elif (enc["type"] == "rot13"): dnc = solve_rot_13(enc["encoded"])
	else: p.interactive()
	payload = {"decoded": dnc}
	json_send(payload)
p.interactive()