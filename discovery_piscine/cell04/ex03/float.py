#!/usr/bin/env python3

num = float(input("Enter a number: "))
if num.is_integer():
    print(f"{num} is an integer.")
else:
    print(f"{num} is a decimal.")