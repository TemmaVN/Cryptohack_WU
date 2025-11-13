#!/usr/bin/env python3

from Crypto.Util.number import *
from collections import namedtuple
import math

v = namedtuple('v','x y z t')
v1 = v(4,1,3,-1)
v2 = v(2,1,-3,4)
v3 = v(1,0,-2,7)
v4 = v(6,2,9,-5)
print(f'{v1 = }')
v_arr = [v1,v2,v3,v4]

def len_v(vector):
	return math.sqrt(vector.x**2 + vector.y**2 + vector.z**2 + vector.t**2)
def mul_vector(v1,v2):
	return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z + v1.t*v2.t
def sub_vector(v1,v2):
	return v(v1.x-v2.x , v1.y-v2.y , v1.z-v2.z , v1.t-v2.t)
def mul_num(v1,num):
	return v(v1.x*num, v1.y*num, v1.z*num, v1.t*num)

print(f'{len_v(v1) = }')
u_arr = []
for i in range(0,len(v_arr)):
	uij = v_arr[i]
	for j in range(0,i):
		vi_uj = mul_vector(v_arr[i],u_arr[j])
		uj_2 = mul_vector(u_arr[j],u_arr[j])
		div = vi_uj/uj_2
		tru = mul_num(u_arr[j],div)
		uij = sub_vector(uij,tru)
	u_arr.append(uij)

print(f'{u_arr = }')
