from collections import defaultdict, deque


def read_input():
    lines = []
    with open("input") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return  lines

# lines = [
#     "..@@.@@@@.",
#     "@@@.@.@.@@",
#     "@@@@@.@.@@",
#     "@.@@@@..@.",
#     "@@.@@@@.@@",
#     ".@@@@@@@.@",
#     ".@.@.@.@@@",
#     "@.@@@.@@@@",
#     ".@@@@@@@@.",
#     "@.@.@@@.@."
# ]

lines = read_input()

def is_paper_roll(x, y, lines):
    if lines[y][x] == "@":
        return True
    return False

def get_adjacent(x, y, lines):
    adjacent = set()
    # up
    if y > 0:
        if is_paper_roll(x, y-1, lines):
            adjacent.add((x, y-1))
    # down
    if y < len(lines) - 1:
        if is_paper_roll(x, y+1, lines):
            adjacent.add((x, y+1))
    # left
    if x > 0:
        if is_paper_roll(x-1, y, lines):
            adjacent.add((x-1, y))
    # right
    if x < len(lines[0]) - 1:
        if is_paper_roll(x+1, y, lines):
            adjacent.add((x+1, y))
    # up/left
    if y > 0 and x > 0:
        if is_paper_roll(x - 1, y-1, lines):
            adjacent.add((x - 1, y-1))
    # up/right
    if y > 0 and x < len(lines[0]) - 1:
        if is_paper_roll(x + 1, y - 1, lines):
            adjacent.add((x + 1, y - 1))
    # down/left
    if y < len(lines) - 1 and x > 0:
        if is_paper_roll(x - 1, y + 1, lines):
            adjacent.add((x - 1, y + 1))
    # down/right
    if y < len(lines) - 1 and x < len(lines[0]) - 1:
        if is_paper_roll(x + 1, y + 1, lines):
            adjacent.add((x + 1, y + 1))
    return adjacent

nodes = set()
neighbors = defaultdict(set)
removable = deque()
removed = set()

for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == "@":
            nodes.add((x, y))
            adjacent = get_adjacent(x, y, lines)
            if len(adjacent) < 4:
                removable.append((x,y))
            neighbors[(x,y)] = neighbors[(x,y)].union(adjacent)

while True:
    try:
        node_to_remove = removable.pop()
    except IndexError:
        # no more nodes to remove.
        print(f"Removed paper rolls: {len(removed)}")
        break

    if node_to_remove not in removed:
        nodes.remove(node_to_remove)
        for neighbor in neighbors[node_to_remove]:
            neighbors[neighbor].remove(node_to_remove)
            if len(neighbors[neighbor]) < 4:
                removable.append(neighbor)
        removed.add(node_to_remove)
