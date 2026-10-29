#!/usr/bin/env python3

original_array = [2, 8, 9, 48, 8, 22, -12, 2]
new_array1 = [i + 2 for i in original_array]
new_array2 = [i for i in new_array1 if i > 5]
set = set(new_array2)

print(original_array)
print(set)