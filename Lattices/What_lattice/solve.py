#!/usr/bin/env python3

import math
import time

def solve(arr):
	if len(arr) != len(arr[0]):
		return None
	for i in range(1,len(arr)):
		tester = []
		for j in range(i,len(arr)):
			tester.append(arr[j][i-1]/arr[i-1][i-1])
		for j in range(i,len(arr)):
			for t in range(i-1,len(arr)):
				arr[j][t] -= arr[i-1][t] * tester[j-i]
	res = 1
	for i in range(len(arr)):
		res *= arr[i][i]
	return res

M = [[6,2,-3],[5,1,4],[2,7,1]]
print(f'{solve(M) = }')