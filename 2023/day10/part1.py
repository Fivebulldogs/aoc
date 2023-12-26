from dataclasses import dataclass
from enum import Enum

# Trying a variant of Kruskal's minimum spanning tree

input = None
with open("input.txt") as f:
    input = f.readlines()

# input = ["7-F7-", ".FJ|7", "SJLL7", "|F--J", "LJ.LJ"]


@dataclass(frozen=True)
class Pos:
    x: int
    y: int
    pipe: str
    steps: int = 0


def find_start_pos(input):
    for y, line in enumerate(input):
        for x, v in enumerate(line.strip()):
            if v == "S":
                # check the next pos to decide dir
                return Pos(x, y, "S")


def find_next_pos(cur_pos, prev_pos):
    # use clockwise movement
    match cur_pos.pipe:
        case "|":
            if cur_pos.y == prev_pos.y + 1:
                # we're moving down
                next_pipe = input[cur_pos.y + 1][cur_pos.x]
                next_pos = Pos(
                    cur_pos.x, cur_pos.y + 1, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                # we're moving up
                next_pipe = input[cur_pos.y - 1][cur_pos.x]
                next_pos = Pos(
                    cur_pos.x, cur_pos.y - 1, next_pipe, steps=cur_pos.steps + 1
                )
        case "-":
            if cur_pos.x == prev_pos.x - 1:
                # we're moving left
                next_pipe = input[cur_pos.y][cur_pos.x - 1]
                next_pos = Pos(
                    cur_pos.x - 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                # we're moving right
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                next_pos = Pos(
                    cur_pos.x + 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                )
        case "L":
            if cur_pos.x == prev_pos.x - 1:
                # we're moving up (from right)
                next_pipe = input[cur_pos.y - 1][cur_pos.x]
                next_pos = Pos(
                    cur_pos.x, cur_pos.y - 1, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                # we're moving right (from above)
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                next_pos = Pos(
                    cur_pos.x + 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                )
        case "J":
            if cur_pos.x == prev_pos.x + 1:
                # we're moving up (from left)
                next_pipe = input[cur_pos.y - 1][cur_pos.x]
                next_pos = Pos(
                    cur_pos.x, cur_pos.y - 1, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                # we're moving left (from above)
                next_pipe = input[cur_pos.y][cur_pos.x - 1]
                next_pos = Pos(
                    cur_pos.x - 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                )
        case "7":
            if cur_pos.x == prev_pos.x + 1:
                # we're moving down (from left)
                next_pipe = input[cur_pos.y + 1][cur_pos.x]
                next_pos = Pos(
                    cur_pos.x, cur_pos.y + 1, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                # we're moving left (from below)
                next_pipe = input[cur_pos.y][cur_pos.x - 1]
                next_pos = Pos(
                    cur_pos.x - 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                )
        case "F":
            if cur_pos.x == prev_pos.x - 1:
                # we're moving down (from right)
                next_pipe = input[cur_pos.y + 1][cur_pos.x]
                next_pos = Pos(
                    cur_pos.x, cur_pos.y + 1, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                # we're moving right (from below)
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                next_pos = Pos(
                    cur_pos.x + 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                )
        case ".":
            raise Exception(f"'.' at {cur_pos}. What? prev_pos is {prev_pos}")
        case "S":
            # check above and right (works for the 2ns example and the real input :)
            next_pipe = input[cur_pos.y - 1][cur_pos.x]
            if next_pipe in ["7", "F", "|"]:
                # above
                next_pos = Pos(
                    cur_pos.x, cur_pos.y - 1, next_pipe, steps=cur_pos.steps + 1
                )
            else:
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                if next_pipe in ["7", "J", "-"]:
                    # right
                    next_pos = Pos(
                        cur_pos.x + 1, cur_pos.y, next_pipe, steps=cur_pos.steps + 1
                    )
    if next_pos.pipe == "S":
        # We're back at S again
        return (None, None)

    return (next_pos, cur_pos)


def trace_positions(input):
    start_pos = find_start_pos(input)
    print("Starting at", start_pos)
    cur_pos = start_pos
    prev_pos = None
    traced_positions = []
    while cur_pos is not None:
        # print(cur_pos)
        traced_positions.append(cur_pos)
        (cur_pos, prev_pos) = find_next_pos(cur_pos, prev_pos)

    return traced_positions


traced_positions = trace_positions(input)
print(len(traced_positions) / 2)
