#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import *
import hashlib


def is_pkcs7_padded(message):
  padding = message[-message[-1]:]
  return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
  # Derive AES key from shared secret
  sha1 = hashlib.sha1()
  sha1.update(str(shared_secret).encode('ascii'))
  key = sha1.digest()[:16]
  # Decrypt flag
  ciphertext = bytes.fromhex(ciphertext)
  iv = bytes.fromhex(iv)
  cipher = AES.new(key, AES.MODE_CBC, iv)
  plaintext = cipher.decrypt(ciphertext)

  if is_pkcs7_padded(plaintext):
    return unpad(plaintext, 16).decode('ascii')
  else:
    return plaintext.decode('ascii')


from pwn import *
io = remote('socket.cryptohack.org',13378)
import json
def json_recv():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

def json_send(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

io.recvuntil(b'Alice: ')
Alice_Intercepted = json_recv()
print(f'{Alice_Intercepted = }')
io.recvuntil(b'Bob: ')
Bob_Intercepted = json_recv()
print(f'{Bob_Intercepted = }')
io.recvuntil(b'Alice: ')
Alice_enc = json_recv()
print(f'{Alice_enc = }')
p = int(Alice_Intercepted['p'],16)
A = int(Alice_Intercepted['A'],16)
B = int(Bob_Intercepted['B'],16)
A_send = hex((A*inverse(4,p))%p)
fake_p = 21161033472192524829557170410776298658794639108376130676557783015578090330844472167861788371083170940722591241807108382859295872641348645166391260040395583908986502774347856154314632614857393087562331369896964916313777278292965202780626304839725254323083321245935920345445760469315716688808181386083935737705284353395869520861742156127496385090743602309049820934917134755461873012945704938955132724663075880436995904093654709349552656965610546540372048421026608925808493978164019986593442564905462745669412326023291812269608558332157759989142549649265359278848084868920655698461242425344000000000000000000000000000000000000000000000000000000000000000000000000000001
payload = {'p': hex(fake_p), 'g': '0x02', 'A': Alice_Intercepted['A']}
json_send(payload)
from sympy.ntheory.residue_ntheory import discrete_log
io.recvuntil(b'Bob says to you: ')
New_B = int(json_recv()['B'],16)
b = discrete_log(fake_p,New_B,0x02)
print(f'{b = }')
shared_secret = pow(A,b,p)
flag = decrypt_flag(shared_secret,Alice_enc['iv'],Alice_enc['encrypted'])
print(f'{flag = }')

io.interactive()
