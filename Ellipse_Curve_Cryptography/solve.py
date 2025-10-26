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

S_d = Sqrt_mod(D,p)
P = Point(x=150539742778301973051821701104483481547633426221667233354502145375756642, y=7213228269545098887984115976819188759113890684398775317815800823633590)
a = 2 
b = -2*Sqrt_mod(S_d*P.y + P.x,p)
c = P.y*S_d
print(f'{Solve_pt_b_2(a,b,c) = }')