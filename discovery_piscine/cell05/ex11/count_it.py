#!/usr/bin/env python3

import sys

argc = sys.argv[1:]

if not argc:
    print("None")
else:
    print(f"parameter: {len(argc)}")
    for arg in argc:
        print(f"{arg}: {len(arg)}")