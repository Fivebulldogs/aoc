from collections import deque
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

possible_design_count = 0
for i, design in enumerate(designs):
    print("design", i + 1, "of", len(designs))
    design_feasible = False
    q = deque()
    q.append(design)
    visited_remaining_designs = set()
    while not design_feasible:
        try:
            remaining_design = q.pop()
            for pattern in patterns:
                reg_pattern = re.compile(pattern)
                match = reg_pattern.match(remaining_design)
                if match:
                    span = match.span()
                    new_remaining_design = remaining_design[span[1] :]
                    if new_remaining_design == "":
                        possible_design_count += 1
                        design_feasible = True
                        break
                    else:
                        if new_remaining_design not in visited_remaining_designs:
                            q.append(new_remaining_design)
                            visited_remaining_designs.add(new_remaining_design)
                if design_feasible:
                    break
        except IndexError:
            break
print("possible_design_count", possible_design_count)
