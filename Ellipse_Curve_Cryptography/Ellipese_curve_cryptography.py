#!/usr/bin/env python3

from Crypto.Util.number import *
from collections import namedtuple

Point = namedtuple("Point","x y")
Point_0 = Point(0,0)

def Is_zero(P : Point):
	if P.x == 0 and P.y == 0:
		return True
	return False 

p = 9739
a = 497
b = 1768

def Point_add(P1: Point, P2: Point):
	if Is_zero(P1): return P2
	if Is_zero(P2): return P1
	if P1.x == P2.x and  P1.y == -P2.y: return Point(0,0)
	else:
		tg = inverse((P2.x - P1.x)%p,p)
		l = (((P2.y - P1.y)%p)*tg)%p 
		if P1.x == P2.x and P1.y == P2.y: 
			test = inverse(2*P1.y,p)
			l = ((3 * P1.x**2 + a) * test)%p 
		x3 = (l**2 - P1.x - P2.x)%p
		y3 = (l*(P1.x - x3) - P1.y)%p
	return Point(x3,y3)

def Point_mul(P1: Point, n: int):
	res = Point(0,0)
	while n > 0:
		if n&1: res = Point_add(res,P1)
		P1 = Point_add(P1,P1)
		n >>= 1
	return res

X = Point(5323,5438)
Y = Point(8669,740)
print(Point_add(X,X))
print(Point_mul(X,1337))