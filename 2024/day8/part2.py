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


def calc_antinodes(pos, row_diff, col_diff, row_count, col_count):
    antinodes = set()
    antinode = Pos(pos.row, pos.col)
    while (
        antinode.row >= 0
        and antinode.col >= 0
        and antinode.row < row_count
        and antinode.col < col_count
    ):
        antinodes.add(antinode)
        antinode = Pos(antinode.row + row_diff, antinode.col + col_diff)
    return antinodes


lines = read_lines("input.txt")
row_count = len(lines)
col_count = len(lines[0])
fm = create_frequency_map(lines)

antinodes = set()
for freq, positions in fm.items():
    for pos1, pos2 in combinations(positions, 2):
        row_diff = pos2.row - pos1.row
        col_diff = pos2.col - pos1.col

        antinodes_pos1 = calc_antinodes(
            pos1, -row_diff, -col_diff, row_count, col_count
        )
        antinodes.update(antinodes_pos1)

        antinodes_pos2 = calc_antinodes(pos2, row_diff, col_diff, row_count, col_count)
        antinodes.update(antinodes_pos2)

print("antinode_count", len(antinodes))
