#!/usr/bin/env python3

encs = []
with open('flag.enc','r') as f:
	for i in range(50):
		encs.append(f.readline().rstrip())

print(f'{encs[2] = }')
idx = 0
plain = '' 
while True:
	the_chr = ''
	for i in range(8):
		the_chr += encs[(idx + i)%50][idx//50]
	plain += chr(int(the_chr,2))
	print(f'{the_chr = }')
	print(f'{int(the_chr,2) = }')
	print(f'{plain = }')
	if input("Oke fen: ") == 'y':
		break 
	idx += 8
print(f'{plain = }')