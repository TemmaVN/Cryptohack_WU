#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import json

io = remote('socket.cryptohack.org',13421)
def send_json(data):
	payload = json.dumps(data).encode()
	io.sendline(payload)

def recv_json():
	data = io.recvline().decode().rstrip()
	return json.loads(data)

io.recvline()
send_json({"option": "encrypt"})
ct = recv_json()["ct"]
iv = bytes.fromhex(ct[:32])
ct = bytes.fromhex(ct[32:])
log.info(f'{iv = }')
log.info(f'{ct = }')

send_json({"option": "unpad","ct": (iv+ct).hex()})
io.interactive()

'''
import json
from tqdm import tqdm
from utils.utils import PrintingSocket, get_blocks, xor_strings, hex_to_ascii

ADDR = ('socket.cryptohack.org', 13421)
ENCRYPT = {"option": "encrypt"}
UNPAD = lambda ct: {"option": "unpad", "ct": ct}
CHECK = lambda msg: {"option": "check", "message": msg}

def ints_to_hex(int_list):
    ret = ""
    for n in int_list:
        ret += hex(n)[2:].zfill(2)
    return ret

def fix_xor_vals(xor_vals, n):
    out = []
    for i in xor_vals:
        out.append(i ^ n ^ n-1)
    return out

def main():
    xor_vals = []
    deciphered = []
    processed = []

    with PrintingSocket() as s:
        s.connect(ADDR)
        s.recv_print()
        s.send_dict(ENCRYPT)
        iv, ct, ct2 = get_blocks(json.loads(s.recv_print().decode())["ct"])
        curr_ct = ct
        for i in range(2):
            for pad_discovered in tqdm(range(1, 17)):
                xor_vals = fix_xor_vals(xor_vals, pad_discovered)
                for i in range(256):
                    to_send = iv[:(16 - pad_discovered)*2] + ints_to_hex([i] + xor_vals)
                    s.send_dict(UNPAD(to_send+curr_ct))
                    res = json.loads(s.recv())["result"]
                    if res:
                        xor_vals.insert(0, i)
                        deciphered.append(i ^ pad_discovered ^ int(iv[
                            (16 - pad_discovered)*2:(16 - pad_discovered + 1)*2], 16))
                        break
            xor_vals = []
            curr_ct = ct2
            iv = ct
            processed += deciphered[::-1]
            deciphered = []
        final_message = hex_to_ascii(ints_to_hex(processed))
        s.send_print_dict(CHECK(final_message))
        s.recv_print()
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
'''