#!/usr/bin/env python3

import sys

if len(sys.argv) != 2 or 'z' not in sys.argv[1]:
    print("none")
else:
    print('z' * sys.argv[1].count('z'))