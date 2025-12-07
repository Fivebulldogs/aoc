import re
from collections import defaultdict


def read_input():
    lines = []
    with open("input") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return lines


# manifold = [
#     ".......S.......",
#     "...............",
#     ".......^.......",
#     "...............",
#     "......^.^......",
#     "...............",
#     ".....^.^.^.....",
#     "...............",
#     "....^.^...^....",
#     "...............",
#     "...^.^...^.^...",
#     "...............",
#     "..^...^.....^..",
#     "...............",
#     ".^.^.^.^.^...^.",
#     "..............."]

manifold = read_input()


def get_beam_positions(row_idx, manifold, beam_positions):
    row_splits = 0
    if row_idx > 0:
        for prev_row_beam_pos in beam_positions[row_idx - 1]:
            pos_val = manifold[row_idx][prev_row_beam_pos]
            pos_to_add = None
            if pos_val == ".":
                # space
                beam_positions[row_idx].add(prev_row_beam_pos)
            else:
                # splitter
                beam_positions[row_idx].add(prev_row_beam_pos - 1)
                beam_positions[row_idx].add(prev_row_beam_pos + 1)
                row_splits += 1
    else:
        start_pos = re.search("S", manifold[0]).span()[0]
        beam_positions[0] = [start_pos]
    return row_splits


beam_positions = defaultdict(set)
splits = 0
for row_idx, row in enumerate(manifold):
    row_splits = get_beam_positions(row_idx, manifold, beam_positions)
    splits += row_splits
print("Splits", splits)
