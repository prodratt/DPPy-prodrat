#!/usr/bin/env python3

i = 0
while i <= 10:
    row = []
    j = 0
    while j <= 10:
        row.append(str(i * j))
        j += 1
    print(f"Table de {i}: " + " ".join(row))
    i += 1
       