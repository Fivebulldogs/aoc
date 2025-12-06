import functools
import operator
from collections import defaultdict


def read_input():
    nums = []
    ops = []
    with open("input") as f:
        line = f.readline()
        while line:
            if not line.startswith("+") and not line.startswith("*"):
                nums.append(line.strip("\n"))
            else:
                ops = line.strip().split()
            line = f.readline()
    return nums, ops


def get_separator_cols(nums):
    space_positions = defaultdict(set)
    for i, row in enumerate(nums):
        for j, col in enumerate(row):
            if col == " ":
                space_positions[i].add(j)

    common_spaces = set(space_positions[0])
    for i in range(1, len(numbers)):
        common_spaces.intersection_update(space_positions[i])
    return common_spaces


operations = ["*", "+", "*", "+"]
numbers = ["123 328  51 64",
           " 45 64  387 23",
           "  6 98  215 314"]

numbers, operations = read_input()
separator_cols = get_separator_cols(numbers)

cols = defaultdict(list)
for i, row in enumerate(numbers):
    for j, col in enumerate(row):
        if j in separator_cols:
            cols[j] = ['0']
        elif col != " ":
            cols[j].append(col)

grand_total = 0
op_idx = 0
problem_vals = []
problem_result = 0
for i, col in sorted(cols.items()):
    if i not in separator_cols:
        val = int("".join(col))
        problem_vals.append(val)

    if i in separator_cols or i == len(cols.values()) - 1:
        op = operations[op_idx]
        problem_result = 0
        if op == "+":
            problem_result = sum(problem_vals)
        else:
            problem_result = functools.reduce(operator.mul, problem_vals, 1)
        op_idx += 1
        problem_vals = []
        grand_total += problem_result
print("Grand total:", grand_total)
