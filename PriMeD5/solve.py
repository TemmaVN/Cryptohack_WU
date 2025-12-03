#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l, isPrime, getPrime
from pwn import *
from Crypto.Hash import MD5
import hashlib
from tqdm import tqdm
import json
import math

msg1 = bytes.fromhex("0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef")
msg2 = bytes.fromhex("0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef")

print(f'{msg1 == msg2}')
print(hashlib.md5(msg1).hexdigest() == hashlib.md5(msg2).hexdigest())  # e7e62dda57560dea3d4dfd91b91f6a79
print(f'{b2l(msg1) % 2 = }')

send1 = b2l(msg1)
send2 = b2l(msg2)


for z in tqdm(range(1,10000000,2)):
	send1 = b2l(msg1 + l2b(z))
	send2 = b2l(msg2 + l2b(z))
	if isPrime(send1) and not isPrime(send2):
		break

print(f'{send1 = }')
print(f'{send2 = }')
a = 1145145015592186154220610422455827107140605136426924830632830555848174108613055810294857749111347602060239737258558590711070492689
print(f'{math.gcd(a,send2) == a}')

io = remote('socket.cryptohack.org',13392)

def send_json(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

payload = {"option": "sign","prime" : str(send1)}
send_json(payload)
io.recvline()
sign = recv_json()['signature']
print(f'{sign = }')
payload = {"option": "check", "prime": str(send2), "signature": sign, "a": str(a)}
send_json(payload)
io.interactive()