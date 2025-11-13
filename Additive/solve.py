#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
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
io = remote('socket.cryptohack.org',13380)
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

from Crypto.Util.number import *
p = int(Alice_Intercepted['p'],16)
A = int(Alice_Intercepted['A'],16)
g = int(Alice_Intercepted['g'],16)
a = (inverse(g,p)*A)%p
shared_secret = (int(Bob_Intercepted['B'],16)*a)%p 
flag = decrypt_flag(shared_secret,Alice_enc['iv'],Alice_enc['encrypted'])
print(f'{flag = }')
io.interactive()
