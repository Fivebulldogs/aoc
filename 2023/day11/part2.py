from collections import defaultdict


def read_input():
    lines = []
    with open("input.txt") as f:
        for line in f.readlines():
            lines.append(line.strip())
    return lines


expansion_factor = 1000000
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


def get_galaxy_map(input):
    non_empty_lines = set()
    non_empty_cols = set()
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == "#":
                non_empty_lines.add(y)
                non_empty_cols.add(x)

    galaxy_map = defaultdict(list)
    i = 0
    j = 0
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if x not in non_empty_cols:
                # x is an empty col, add x more times
                i += expansion_factor - 1
            elif c == "#":
                print(y, x, j, i)
                galaxy_map[j].append(i)
            i += 1

        if y not in non_empty_lines:
            j += expansion_factor - 1
        j += 1
        i = 0

    return galaxy_map


def get_galaxy_positions(galaxy_map):
    galaxy_positions = []
    for y, x_vec in galaxy_map.items():
        for x in x_vec:
            galaxy_positions.append((x, y))
    return galaxy_positions


def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


galaxy_map = get_galaxy_map(input)
galaxy_positions = get_galaxy_positions(galaxy_map)
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
        # print(pos1, pos2, dist)
        pair_count += 1

print(pair_count, dist_sum)
print(dist_sum)
