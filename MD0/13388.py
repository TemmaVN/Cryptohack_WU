#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import json

FLAG = "crypto{???????????????}"


def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def hash(data):
    data = pad(data, 16)
    out = b"\x00" * 16
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        out = bxor(AES.new(blk, AES.MODE_ECB).encrypt(out), out)
    return out


class Challenge():
    def __init__(self):
        self.before_input = "You'll never forge my signatures!\n"
        self.key = os.urandom(16)

    def challenge(self, msg):
        if "option" not in msg:
            return {"error": "You must send an option to this server."}

        elif msg["option"] == "sign":
            data = bytes.fromhex(msg["message"])
            if b"admin=True" in data:
                return {"error": "Unauthorized to sign message"}
            sig = hash(self.key + data)

            return {"signature": sig.hex()}

        elif msg["option"] == "get_flag":
            sent_sig = bytes.fromhex(msg["signature"])
            data = bytes.fromhex(msg["message"])
            real_sig = hash(self.key + data)
            print(f'{real_sig.hex() = }')
            if real_sig != sent_sig:
                return {"error": "Invalid signature"}

            if b"admin=True" in data:
                return {"flag": FLAG}
            else:
                return {"error": "Unauthorized to get flag"}

        else:
            return {"error": "Invalid option"}

chall = Challenge()
while True:
    msg = json.loads(input())
    print(chall.challenge(msg))
