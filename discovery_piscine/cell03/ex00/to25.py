#!/usr/bin/env python3

input_num = int(input("Enter a number less than 25: "))
if input_num < 25:
    while input_num <= 25:
        print("Inside the loop, my variable is: " + str(input_num))
        input_num += 1

else:
    print("error: The number is not less than 25")
