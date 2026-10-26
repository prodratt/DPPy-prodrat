#!/usr/bin/env python3

num1 = input("Enter the first number: ")
num2 = input("Enter the second number: ")
num = str(int(num1) * int(num2))
print("The product of " + num1 + " and " + num2 + " is: " + num)

if int(num) == 0:
    print("This number is both negative and positive")
elif int(num) < 0:
    print("This number is negative")
else:
    print("This number is positive")

