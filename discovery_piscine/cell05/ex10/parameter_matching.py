#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("None")
else:
    word = input("What was a parameters? ")
    if word == sys.argv[1]:
        print("Good job, you got it!")
    else:
        print("Nope, try again")