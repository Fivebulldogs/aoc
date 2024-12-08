from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations


@dataclass(unsafe_hash=True)
class Pos:
    row: int = None
    col: int = None


def read_lines(filename):
    with open(filename) as f:
        m = []
        line = f.readline()
        while line:
            m.append(list(line.strip()))
            line = f.readline()
        return m


def create_frequency_map(lines):
    fm = defaultdict(list)
    for i, row in enumerate(lines):
        for j, col in enumerate(row):
            if col != ".":
                fm[col].append(Pos(row=i, col=j))
    return fm


def get_antinodes(pos1, pos2):
    # does the antinodes on the line of these
    # positions fit on the map?
    row_diff = abs(pos1.row - pos2.row)
    col_diff = abs(pos1.col - pos2.col)

    antinode_1 = Pos()
    antinode_2 = Pos()
    if pos1.row < pos2.row:
        antinode_1.row = pos1.row - row_diff
        antinode_2.row = pos2.row + row_diff
    elif pos1.row > pos2.row:
        antinode_1.row = pos1.row + row_diff
        antinode_2.row = pos2.row - row_diff
    else:
        # same row
        antinode_1.row, antinode_2.row = pos1.row

    if pos1.col < pos2.col:
        antinode_1.col = pos1.col - col_diff
        antinode_2.col = pos2.col + col_diff
    elif pos1.col > pos2.col:
        antinode_1.col = pos1.col + col_diff
        antinode_2.col = pos2.col - col_diff
    else:
        # same col
        antinode_1.col, antinode_2.col = pos1.col

    return (antinode_1, antinode_2)


lines = read_lines("input.txt")
row_count = len(lines)
col_count = len(lines[0])
fm = create_frequency_map(lines)

antinodes = set()
for freq, positions in fm.items():
    for pos1, pos2 in combinations(positions, 2):
        (antinode_1, antinode_2) = get_antinodes(pos1, pos2)
        if (antinode_1.row >= 0 and antinode_1.row < row_count) and (
            antinode_1.col >= 0 and antinode_1.col < col_count
        ):
            antinodes.add(antinode_1)
        if (antinode_2.row >= 0 and antinode_2.row < row_count) and (
            antinode_2.col >= 0 and antinode_2.col < col_count
        ):
            antinodes.add(antinode_2)

print("antinode_count", len(antinodes))
