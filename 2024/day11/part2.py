# input = "1750884 193 866395 7 1158 31 35216 0"
from functools import cache


# input = "125 17"
input = "1750884 193 866395 7 1158 31 35216 0"
target_level = 75


@cache
def count_leaves(val, level):
    if level == target_level:
        return 1

    if val == "0":
        return count_leaves("1", level + 1)
    elif len(val) % 2 == 0:
        half_len = int(len(val) / 2)
        left = val[:half_len]
        left_val = left.lstrip("0")
        right = val[half_len:]
        stripped_right = right.lstrip("0")
        right_val = stripped_right if len(stripped_right) > 0 else "0"
        return count_leaves(left_val, level + 1) + count_leaves(right_val, level + 1)
    else:
        return count_leaves(str(int(val) * 2024), level + 1)


result = 0
level = 0
for val in input.split(" "):
    result += count_leaves(val, 0)

print("result", result)
