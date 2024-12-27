from collections import defaultdict, deque
from functools import cache
import re


def read_file(filename):
    patterns = []
    designs = []
    with open(filename) as f:
        line = f.readline()
        for pattern in line.split(","):
            patterns.append(pattern.strip())

        line = f.readline()
        line = f.readline()
        while line:
            design = line.strip()
            designs.append(design)
            line = f.readline()

    return (patterns, designs)


(patterns, designs) = read_file("input")


@cache
def count_arrangements(s: str):
    if s == "":
        return 1

    arrangement_count = 0
    match_found = False
    for pattern in patterns:
        reg_pattern = re.compile(pattern)
        match = reg_pattern.match(s)
        if match:
            match_found = True
            span = match.span()
            remaining_s = s[span[1] :]
            arrangement_count += count_arrangements(remaining_s)

    if not match_found:
        return 0

    return arrangement_count


total_arrangement_count = 0
for i, design in enumerate(designs):
    total_arrangement_count += count_arrangements(design)

print("total_arrangement_count", total_arrangement_count)
