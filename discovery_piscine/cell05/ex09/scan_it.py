#!/usr/bin/env python3

import sys

if len(sys.argv) == 3 and sys.argv[1] and sys.argv[2]:
    print(sys.argv[2].count(sys.argv[1]))
else:
    print("none")