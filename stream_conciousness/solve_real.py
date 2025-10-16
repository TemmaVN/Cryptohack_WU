#!/usr/bin/env python3

import requests
import json
from tqdm import tqdm
import time

URL = r"https://aes.cryptohack.org/stream_consciousness/encrypt"

# run this when starting the challenge
def get_cts():
    all_cts = set()
    for _ in tqdm(range(60)):
        all_cts.add(json.loads(requests.get(URL).text)["ciphertext"])

    with open("cts.txt", "w") as f:
        f.write('\n'.join(all_cts))
    
def main():
    with open("cts.txt", "r") as f:
        all_cts = f.readlines()

    keys = set()
    
    for ct in all_cts:
        keys.add(xor_strings(ct, ascii_to_hex(r"crypto{")))
    
    master_key = 0
    
    key_candidates = [[], []]
    
    for key in keys:
        for ct in all_cts:
            txt = hex_to_ascii(xor_strings(key, ct))
            if "I shall" in txt:
                key_candidates[0].append(key)
            if "Love, p" in txt:
                key_candidates[1].append(key)
    
    for i in key_candidates[0]:
        for j in key_candidates[1]:
            if i == j:
                master_key = i

    while True:
        if 'y' == input("Is the flag here? [y] "):
            break
        for i in range(256):
            attempt_key = master_key + ints_to_hex([i])
            txt_batch = []
            for ct in all_cts:
                try:
                    txt = hex_to_ascii(xor_strings(attempt_key, ct))
                    txt_batch.append(txt)
                except UnicodeDecodeError:
                    break
                if r"crypto{" in txt:
                    print("Curr flag status: ", txt, "Curr Master: ", master_key)
               
            if txt_batch:
                print(txt_batch)               
                if 'y' == input("Does it look legit? [y] "):
                    master_key += ints_to_hex([i])
                    break
    
if __name__ == "__main__":
    main()