#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import *
import numpy as np 
import matplotlib.pyplot as plt
import imageio

def get_flag(input_data):
	flag = np.array(imageio.imread('/home/temma/Documents/Cryptohack/lemur_xor/flag.png'), dtype = np.int64)
	lemur = np.array(imageio.imread('/home/temma/Documents/Cryptohack/lemur_xor/lemur.png'), dtype = np.int64)

	plt.imshow(flag ^ lemur)
	plt.show()

	return None

input_data = None
get_flag(input_data)

