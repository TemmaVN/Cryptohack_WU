#!/usr/bin/env python3

from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from ast import literal_eval

options = ['sign', 'get_flag']

def bxor(a,b):
	return bytes(x ^ y for x,y in zip(a,b))

io = remote('socket.cryptohack.org',13388)
# io = process(['python3','13388.py'])

def send_payload(option, msg, sign = None):
	if option == options[0]:
		data = {'option': option, 'message' : msg}
	else:
		data = {'option': option, 'message' : msg, 'signature': sign}
	payload = json.dumps(data).encode()
	io.sendline(payload)

def recv_json():
    return literal_eval(io.recvline().decode().rstrip())

fake_admin = b'\x00'*16
real_admin = b'admin=True'
real_admin_pad = pad(real_admin,16)  
send_payload(options[0],fake_admin.hex())
io.recvline()
sign = bytes.fromhex(recv_json()['signature'])
sign = bxor(AES.new(real_admin_pad,AES.MODE_ECB).encrypt(sign),sign).hex()
print(f'{sign = }')
send_payload(options[1],(pad(fake_admin,16) + real_admin).hex(), sign)
io.interactive()

