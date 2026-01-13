#!/usr/bin/env python3

from pwn import *
from Crypto.Hash import MD5
import os
import json

option = ['insert_key','unlock']
io = remote('socket.cryptohack.org',13397)

def send_json(choose,data):
	if( choose == option[0]): payload = {'option': choose ,'key': data}
	else: payload = {'option': choose} 
	payload = json.dumps(payload).encode()
	io.sendline(payload)

KEY_START = b"CryptoHack Secure Safe"
'''
Find md5 hash collision such that one starts with KEY_START and one doesn't
'''
# We get :
from tqdm import tqdm 
k1 = "43727970746f4861636b205365637572652053616665300a08de6e639eb76baa3f782925580a654ad735580c928d0e6936fecd35ebd5ac2d6bc4608b6e55239ddee23a8ae2c6bdcdf57745c78aef60b46903e9b3eb4e128ad05ab9f459839ccd8374ca53aa802edd2cba35bf081d2b7ae96e70787c391cf11bcc226565219236"
k2 = "43727970746f4861636c205365637572652053616665300a08de6e639eb76baa3f782925580a654ad735580c928d0e6936fecd35ebd5ac2d6bc4608b6e55239ddee23a8ae2c6bdcdf57645c78aef60b46903e9b3eb4e128ad05ab9f459839ccd8374ca53aa802edd2cba35bf081d2b7ae96e70787c391cf11bcc226565219236"

for i in range(len(k1)):
	if k1[i] != k2[i]:
		print(f'{i = }')

send_json(option[0],k1)
send_json(option[0],k2)
send_json(option[1],'sajbkasbdjsabd')

io.interactive()