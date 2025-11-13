#!/usr/bin/env python3

from collections import namedtuple
import math
import time

point = namedtuple('point','x y')

def len_point(p1: point):
	return p1.x**2 + p1.y**2

def mul_point(p1: point, p2: point):
	return p1.x*p2.x + p1.y*p2.y

def mul_num(p: point, num: int):
	return point(p.x*num, p.y*num)

def sub_point(p1: point, p2: point):
	return point(p1.x - p2.x, p1.y - p2.y)

def gaussian_reduction(p1: point, p2: point):
	if len_point(p1) > len_point(p2):
		p1, p2 = p2, p1
	m = round(mul_point(p2,p1)/mul_point(p1,p1))
	print(f'{mul_point(p2,p1) = }')
	print(f'{mul_point(p1,p1) = }')
	print(f'{m = }')
	print(f'{p1 = }')
	print(f'{p2 = }')
	while m != 0:
		p2 = sub_point(p2, mul_num(p1,m))
		if len_point(p1) > len_point(p2):
			p1, p2 = p2, p1
		m = round(mul_point(p2,p1)/mul_point(p1,p1))
		print(f'{mul_point(p2,p1) = }')
		print(f'{mul_point(p1,p1) = }')
		print(f'{m = }')
		print(f'{p1 = }')
		print(f'{p2 = }')
		time.sleep(2)
	return p1,p2



p1 = point(846835985,9834798552)
p2 = point(87502093,123094980)
p11, p21 = gaussian_reduction(p1,p2)
print(f'{mul_point(p11,p21) = }')