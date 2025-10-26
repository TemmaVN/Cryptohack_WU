#!/usr/bin/env python3
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

msg = "crypto{bksdbfkdsbkfndsj}"

with open('21.pem') as f:
    key = RSA.importKey(f.read())

cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(msg)

print(ciphertext.hex())

