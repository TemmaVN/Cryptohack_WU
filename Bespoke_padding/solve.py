from pwn import *
import json
from Crypto.Util.number import long_to_bytes,bytes_to_long
#================================== GET THE DATA ==================================#
io = remote('socket.cryptohack.org',13386)
def json_send(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)
def json_recv():
	data = io.recvline().decode().strip()
	return json.loads(data)

io.recvuntil(b'my flag.')
json_send({'option':'get_flag'})
io.recvline()
data = json_recv()
enc = [data['encrypted_flag']]
modul = int(data['modulus'])
a = [data['padding'][0]]
b = [data['padding'][1]]
json_send({'option':'get_flag'})
data = json_recv()
log.info(f'{modul = }')
log.info(f'{type(modul) = }')
enc.append(data['encrypted_flag'])
a.append(data['padding'][0])
b.append(data['padding'][1])
#================================== SOLVE THE CHALLENGE ==================================#
from sage.all import * 

R = PolynomialRing(Zmod(modul),'x')
x = R.gen()
e = 11
f1 = (a[0]*x + b[0])**e - Integer(enc[0])
f2 = (a[1]*x + b[1])**e - Integer(enc[1])
def gcd(f1,f2):
    while f2:
        f1,f2 = f2,f1%f2
    return f1.monic()
g = -gcd(f1,f2).coefficients()[0]
flag = long_to_bytes(int(g))
print(f'Flag: {flag}')
#================================== INTERACTIVE SHELL ==================================#


io.interactive()

