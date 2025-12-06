import functools
import operator
from collections import defaultdict


def read_input():
    nums = defaultdict(list)
    ops = []
    with open("input") as f:
        line = f.readline()
        i = 0
        while line:
            if not line.startswith("+") and not line.startswith("*"):
                for col in line.strip().split():
                    nums[i].append(int(col))
            else:
                ops = line.strip().split()
            line = f.readline()
            i += 1
    return nums, ops


# operations = ["*", "+", "*", "+"]
# numbers = {0: [123, 328, 51, 64],
#            1: [45, 64, 387, 23],
#            2: [6, 98, 215, 314]}

numbers, operations = read_input()
row_count = len(numbers)
col_count = len(numbers[0])
grand_total = 0

for col_idx in range(col_count):
    col = []
    for row_idx in range(row_count):
        col.append(numbers[row_idx][col_idx])
    col_result = 0
    if operations[col_idx] == "+":
        col_result = sum(col)
    else:
        col_result = functools.reduce(operator.mul, col, 1)
    grand_total += col_result

print("Grand total:", grand_total)
