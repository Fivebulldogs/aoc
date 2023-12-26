def read_input():
    lines = []
    with open("input.txt") as f:
        for line in f.readlines():
            lines.append(line.strip())
    return lines


input = read_input()

# input = [
#     "...#......",
#     ".......#..",
#     "#.........",
#     "..........",
#     "......#...",
#     ".#........",
#     ".........#",
#     "..........",
#     ".......#..",
#     "#...#.....",
# ]


def expand_input(input):
    non_empty_lines = set()
    non_empty_cols = set()
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == "#":
                non_empty_lines.add(y)
                non_empty_cols.add(x)

    # print(non_empty_lines)
    # print(non_empty_cols)

    expanded_input = []
    for y, line in enumerate(input):
        expanded_row = ""
        for x, c in enumerate(line):
            expanded_row = f"{expanded_row}{c}"
            if x not in non_empty_cols:
                # x is an empty col
                expanded_row = f"{expanded_row}."
        expanded_input.append(expanded_row)
        if y not in non_empty_lines:
            # add the expanded row again
            expanded_input.append(expanded_row)
    return expanded_input


def get_galaxy_positions(expanded_input):
    galaxy_positions = []
    for y, line in enumerate(expanded_input):
        for x, c in enumerate(line):
            if c == "#":
                galaxy_positions.append((x, y))
    return galaxy_positions


def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


expanded_input = expand_input(input)
galaxy_positions = get_galaxy_positions(expanded_input)
galaxy_positions_count = len(galaxy_positions)
dist_sum = 0
pair_count = 0
for i in range(galaxy_positions_count):
    for j in range(i, galaxy_positions_count):
        if i == j:
            continue
        pos1 = galaxy_positions[i]
        pos2 = galaxy_positions[j]
        dist = get_distance(pos1, pos2)
        dist_sum += dist
        print(pos1, pos2, dist)
        pair_count += 1

# print(pair_count, dist_sum)
print(dist_sum)
