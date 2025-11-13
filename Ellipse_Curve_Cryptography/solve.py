#!/usr/bin/env python3

from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import *
from hashlib import sha1
import random
import os

from collections import namedtuple
# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")
p = 173754216895752892448109692432341061254596347285717132408796456167143559
D = 529
G = Point(29394812077144852405795385333766317269085018265469771684226884125940148,
          94108086667844986046802106544375316173742538919949485639896613738390948)
d = 23
def point_sub(P, Q):
	test_y = (Q.x**2 - D*(Q.y**2))%p 
	test_y_1 = inverse(test_y,p)
	Ry = ((P.y*Q.x - P.x*Q.y)*test_y_1)%p
	Qy_1 = inverse(Q.y,p)
	test_x = (P.y - Q.x*Ry)%p
	Rx = (test_x*Qy_1)%p
	return Point(Rx,Ry)


def Sqrt_mod(a,q):
	if q%4==3: return pow(a,(q+1)//4,q)
	s = 0 
	r = q - 1 
	while r%2 == 0:
		s+=1
		r//=2 
	z = random.randint(2,q-2)
	while pow(z,(q-1)//2,q) == 1:
		z = random.randint(2,q-2)

	m = s 
	c = pow(z,r,q)
	t = pow(a,r,q)
	g = pow(a,(r+1)//2,q)
	while t != 1:
		i = 0
		temp = t
		while temp != 1:
			temp = pow(temp,2,q)
			i+=1 
			if i == m:
				return -1 
		b = pow(c,2**(m-i-1),q)
		g = (g * b)%q 
		t = (t * b * b)%q 
		c = (b*b)%q 
		m = i 
	return min(g,q-g)

def Point_div_2(P: Point):
	Rx, Ry = P.x, P.y 
	y = Sqrt_mod((inverse(d-1,p)*inverse(d+1,p)*(Rx - Ry)%p),p)
	x = (Ry - y**2)%p 
	return Point(x,y)

test = Point(x=15660420594291370535069491844406424967852707131444735568466378459646874, y=160520324418837111973407097622974384638571672119390824076005682782457532)
print(f'{Point_div_2(test) = }')


def Solve_pt_b_2(a,b,c):
	delta = (b**2 - 4*a*c)
	if (delta < 0 ): return -1
	elif delta == 0: 
		tg = inverse(2*a,p)
		return ((-b)*tg)%p
	else:
		tg = inverse(2*a,p)
		x1 = ((-b+Sqrt_mod(delta,p))*tg)%p
		x2 = ((-b-Sqrt_mod(delta,p))*tg)%p 
		return (x1,x2)


enc = {'iv': '64bc75c8b38017e1397c46f85d4e332b', 'encrypted_flag': '13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf'}
Bob_key = Point(x=171226959585314864221294077932510094779925634276949970785138593200069419, y=54353971839516652938533335476115503436865545966356461292708042305317630)
alice_key = Point(x=155781055760279718382374741001148850818103179141959728567110540865590463, y=73794785561346677848810778233901832813072697504335306937799336126503714)

