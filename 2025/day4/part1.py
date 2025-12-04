from fontTools.misc.cython import returns


def read_input():
    lines = []
    with open("input") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return  lines

lines = [
"..@@.@@@@.",
"@@@.@.@.@@",
"@@@@@.@.@@",
"@.@@@@..@.",
"@@.@@@@.@@",
".@@@@@@@.@",
".@.@.@.@@@",
"@.@@@.@@@@",
".@@@@@@@@.",
"@.@.@@@.@."
]

lines = read_input()

def is_paper_roll(x, y, lines):
    if lines[y][x] == "@":
        return 1
    return 0

def get_adjacent(x, y, lines):
    count = 0
    # up
    if y > 0:
        count += is_paper_roll(x, y-1, lines)
    # down
    if y < len(lines) - 1:
        count += is_paper_roll(x, y+1, lines)
    # left
    if x > 0:
        count += is_paper_roll(x-1, y, lines)
    # right
    if x < len(lines[0]) - 1:
        count += is_paper_roll(x+1, y, lines)
    # up/left
    if y > 0 and x > 0:
        count += is_paper_roll(x-1, y-1, lines)
    # up/right
    if y > 0 and x < len(lines[0]) - 1:
        count += is_paper_roll(x+1, y-1, lines)
    # down/left
    if y < len(lines) - 1 and x > 0:
        count += is_paper_roll(x-1, y+1, lines)
    # down/right
    if y < len(lines) - 1 and x < len(lines[0]) - 1:
        count += is_paper_roll(x+1, y+1, lines)
    return count

roll_access_count = 0
for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == "@":
            if get_adjacent(x, y, lines) < 4:
                roll_access_count += 1
                print("ok at", y, x, roll_access_count)
print("Roll access count:", roll_access_count)