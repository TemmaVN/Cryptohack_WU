#!/usr/bin/env python3

# from pwn import *
# import requests
# from Crypto.Cipher import ARC4

# def send_cmd(ciphertext, nonce):
# 	url = 'https://aes.cryptohack.org/oh_snap/send_cmd/'
# 	r = requests.get(url + ciphertext + '/' + nonce + '/')
# 	return r.json()

# print(f'{send_cmd('0'*100,'63727970746f63727970746f') = }')

# ARC4 / RC4 minimal implementation (Python3)

def ksa(key: bytes) -> list:
    """Key-Scheduling Algorithm: trả về permutation S (list 0..255)."""
    keylen = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylen]) & 0xFF
        S[i], S[j] = S[j], S[i]
    return S

def ksa_1(key: list) -> bytes:
	res = b''

print(f'{ksa(b'a') = }')

def prga(S: list):
    """Generator PRGA: yield từng byte keystream (0..255)."""
    i = 0
    j = 0
    # copy S nếu bạn muốn giữ S gốc không đổi
    S = S[:] 
    while True:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xFF]
        yield K

def arc4_keystream(key: bytes, nbytes: int, drop: int = 0) -> bytes:
    """Trả về nbytes keystream. Nếu drop>0 thì bỏ drop byte đầu (RC4-dropN)."""
    S = ksa(key)
    g = prga(S)
    # drop initial bytes if requested (mitigation)
    for _ in range(drop):
        next(g)
    out = bytearray(next(g) for _ in range(nbytes))
    return bytes(out)

# Ví dụ sử dụng:
if __name__ == "__main__":
    key = b"secretkey"
    ks = arc4_keystream(key, 32, drop=256)  # bỏ 256 byte đầu (thường dùng để giảm bias)
    print("keystream (hex):", ks.hex())
