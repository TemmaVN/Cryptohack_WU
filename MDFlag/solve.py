#!/usr/bin/env python3

from pwn import *
import json
import hashlib

# Cấu hình kết nối (Thay đổi theo thông tin server thực tế của bạn)
# Nếu chạy local file, bạn có thể dùng process()
# r = remote('ip-cua-server', port) 
# Ví dụ chạy với file python local:
r = remote('socket.cryptohack.org',13407)

def send_json(data_bytes):
    payload = {
        "option": "message",
        "data": data_bytes.hex()
    }
    r.sendline(json.dumps(payload).encode())
    return r.recvline()

def solve():
    print("[*] Đang tìm độ dài của FLAG...")
    
    flag_length = 0
    
    # Brute-force độ dài từ 1 đến 100
    for length in range(1, 100):
        # Gửi chuỗi byte rỗng (\x00) có độ dài 'length'
        test_data = b'\x00' * length
        
        # Nhận phản hồi
        response = send_json(test_data)
        
        # Parse JSON phản hồi
        try:
            resp_json = json.loads(response.decode())
            
            # Nếu không có lỗi "Bad input", ta đã tìm thấy độ dài tối thiểu
            if "error" not in resp_json:
                flag_length = length
                print(f"[+] Tìm thấy độ dài FLAG: {flag_length}")
                
                # Lưu lại hash của (FLAG ^ \x00) -> Chính là MD5(FLAG)
                flag_hash = resp_json['hash']
                print(f"[+] MD5(FLAG) = {flag_hash}")
                break
        except:
            continue

    if flag_length == 0:
        print("[-] Không tìm thấy độ dài phù hợp.")
        return

    print("\n[*] Thử kiểm tra giả thuyết (Known Plaintext)...")
    
    # Giả sử ta biết flag format là 'crypto{'
    # Ta không thể brute-force từng ký tự vì MD5 avalanche effect (thay đổi 1 bit input, output đổi hoàn toàn).
    # Tuy nhiên, nếu flag có trong wordlist, ta có thể thử offline.
    
    # KỸ THUẬT: VERIFY TOÀN BỘ FLAG
    # Nếu bạn đoán flag là G, hãy gửi data = G.
    # Nếu đúng, server sẽ tính MD5(G ^ G) = MD5(\x00 * length)
    
    # Tính giá trị hash mục tiêu (Target Hash) khi đoán đúng
    null_bytes = b'\x00' * flag_length
    target_hash = hashlib.md5(null_bytes).hexdigest()
    print(f"[*] Target Hash (nếu đoán đúng toàn bộ Flag): {target_hash}")
    
    # Tại đây bạn có thể viết một vòng lặp brute-force nếu không gian mẫu nhỏ
    # Ví dụ thử đoán flag mẫu (đương nhiên sẽ sai với flag thật)
    guess = b'crypto{' + b'A' * (flag_length - 8) + b'}' # Tạo flag giả
    
    # Gửi guess lên server
    resp = send_json(guess)
    resp_json = json.loads(resp.decode())
    
    if "hash" in resp_json and resp_json["hash"] == target_hash:
        print(f"[SUCCESS] Tìm thấy Flag: {guess}")
    else:
        print(f"[-] Guess sai. Hash nhận được: {resp_json.get('hash')}")
        print("[-] Bài này cần brute-force offline hoặc có side-channel khác nếu flag quá dài.")

if __name__ == "__main__":
    solve()
