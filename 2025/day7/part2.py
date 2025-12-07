import functools
import re


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


@functools.cache
def get_timeline_count(row_idx, prev_row_beam_pos):
    if row_idx == len(manifold) - 1:
        return 1
    pos_val = manifold[row_idx][prev_row_beam_pos]
    if pos_val == ".":
        # space
        return get_timeline_count(row_idx + 1, prev_row_beam_pos)
    else:
        # splitter
        return get_timeline_count(row_idx + 1, prev_row_beam_pos - 1) + get_timeline_count(row_idx + 1,
                                                                                           prev_row_beam_pos + 1)
    return timeline_count


start_pos = re.search("S", manifold[0]).span()[0]
timeline_count = get_timeline_count(1, start_pos)
print("timeline count", timeline_count)
