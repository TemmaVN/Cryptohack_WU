#!/usr/bin/env python3
BLOCK_SIZE = 32
from pwn import *
import json

io = remote('socket.cryptohack.org',13405)

def send_two_mess(m1,m2):
    data = {'m1': m1, 'm2': m2}
    payload = json.dumps(data).encode()
    io.sendline(payload)

m1 = b'\x01'*31
m2 = b'\x01'*32
send_two_mess(m1.hex(),m2.hex())
io.interactive()