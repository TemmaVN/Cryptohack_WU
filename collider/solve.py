#!/usr/bin/env python3

from pwn import *
import json
import hashlib

io = remote('socket.cryptohack.org',13389)
def send_recv(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

io.recvline()
b1 = "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
b2 = "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"
data = b"Particle physics (also known as high energy physics) is a branch of physics that studies the nature of the particles that constitute matter and radiation. Although the word particle can refer to various types of very small objects (e.g. protons, gas particles, or even household dust), particle physics usually investigates the irreducibly smallest detectable particles and the fundamental interactions necessary to explain their behaviour."
print(f'{hashlib.md5(data).hexdigest() = }')
request = {
	"document": b1
}
send_recv(request)
request = {
	"document": b2
}
send_recv(request)
io.interactive()