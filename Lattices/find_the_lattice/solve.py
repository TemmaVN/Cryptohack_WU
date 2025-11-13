#!/usr/bin/env python

from collections import namedtuple

point = namedtuple('point', 'x y')
q = 7638232120454925879231554234011842347641017888219021175304217358715878636183252433454896490677496516149889316745664606749499241420160898019203925115292257
h = 2163268902194560093843693572170199707501787797497998463462129592239973581462651622978282637513865274199374452805292639586264791317439029535926401109074800
e = 5605696495253720664142881956908624307570671858477482119657436163663663844731169035682344974286379049123733356009125671924280312532755241162267269123486523

def mul_point(p1: point, p2: point):
	return p1.x*p2.x + p1.y*p2.y

def mul_num(p1: point,num: int):
	return point(p1.x*num, p1.y*num)

def sub_point(p1: point, p2: point):
	return point(p1.x - p2.x, p1.y - p2.y)



def gausses_reduction(p1: point, p2: point):
	if mul_point(p2,p2) < mul_point(p1,p1):
		p2, p1 = p1, p2
	m = round(mul_point(p2,p1)/mul_point(p1,p1))
	while m !=0:
		p2 = sub_point(p2,mul_num(p1,m))
		if mul_point(p2,p2) < mul_point(p1,p1):
			p2,p1 = p1, p2 
		m = round(mul_point(p2,p1)/mul_point(p1,p1))
	return p1, p2

p1 = point(q,0)
p2 = point(h,1)
u,v = gausses_reduction(p1,p2)
f = abs(u.y)
g = abs(u.x)
print(f'{u = }')
print(f'{v = }')


from Crypto.Util.number import inverse, long_to_bytes

def decrypt(h,q,f,g,e):
	a = (f*e) % q
	m = (inverse(f%g,g)*a)%g 
	return long_to_bytes(m)

print(f'{decrypt(h,q,f,g,e) = }')

