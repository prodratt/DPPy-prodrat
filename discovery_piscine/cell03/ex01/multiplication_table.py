#!/usr/bin/env python3

num = int(input("Enter a number: "))
for i in range(1, 10):
    product = num * i
    print(str(i) + " x " + str(num) + " = " + str(product))