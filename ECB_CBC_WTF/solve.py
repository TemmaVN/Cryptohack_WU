#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Cipher import AES

enc = "b3347e942a3c54ae83a574a626d79586848a24ae241e783cecde89223c2d9c83ce73d8e6557051bf74991b15c7c9e97d"

iv = enc[0:32]

c1 = enc[32:64]

c2 = enc[64:96]

print(f'{iv = }')
print(f'{c1 = }')
print(f'{c2 = }')

pl1 = "d04607e45e532f9de0c72b9353b4feb3"
pl2 = "dbbe529e157a270ddb81a8031d0cbdfe"

xor_k = "63727970746f7b3363625f3575636b35"

flag = "crypto{3cb_5uck5_4v01d_17_!!!!!}"


