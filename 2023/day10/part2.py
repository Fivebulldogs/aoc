from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from math import sqrt

# Trying a variant of Kruskal's minimum spanning tree

input = None
with open("input.txt") as f:
    input = f.readlines()

# input = [
#     "...........",
#     ".S-------7.",
#     ".|F-----7|.",
#     ".||.....||.",
#     ".||.....||.",
#     ".|L-7.F-J|.",
#     ".|..|.|..|.",
#     ".L--J.L--J.",
#     "...........",
# ]

# input = [
#     ".F----7F7F7F7F-7....",
#     ".|F--7||||||||FJ....",
#     ".||.FJ||||||||L7....",
#     "FJL7L7LJLJ||LJ.L-7..",
#     "L--J.L7...LJS7F-7L7.",
#     "....F-J..F7FJ|L7L7L7",
#     "....L7.F7||L7|.L7L7|",
#     ".....|FJLJ|FJ|F7|.LJ",
#     "....FJL-7.||.||||...",
#     "....L---J.LJ.LJLJ...",
# ]

# input = [
#     "FF7FSF7F7F7F7F7F---7",
#     "L|LJ||||||||||||F--J",
#     "FL-7LJLJ||||||LJL-77",
#     "F--JF--7||LJLJ7F7FJ-",
#     "L---JF-JLJ.||-FJLJJ7",
#     "|F|F-JF---7F7-L7L|7|",
#     "|FFJF7L7F-JF7|JL---7",
#     "7-L-JL7||F7|L7F-7F7|",
#     "L.L7LFJ|||||FJL7||LJ",
#     "L7JLJL-JLJLJL--JLJ.L",
# ]


@dataclass(frozen=True)
class Pos:
    x: int
    y: int
    pipe: str = ""


def find_start_pos(input):
    for y, line in enumerate(input):
        for x, v in enumerate(line.strip()):
            if v == "S":
                # check the next pos to decide dir
                return Pos(x, y, "S")


def find_next_pos(cur_pos, prev_pos):
    next_pos = None
    # use clockwise movement
    match cur_pos.pipe:
        case "|":
            if cur_pos.y == prev_pos.y + 1:
                # we're moving down
                next_pipe = input[cur_pos.y + 1][cur_pos.x]
                next_pos = Pos(cur_pos.x, cur_pos.y + 1, next_pipe)
            else:
                # we're moving up
                next_pipe = input[cur_pos.y - 1][cur_pos.x]
                next_pos = Pos(cur_pos.x, cur_pos.y - 1, next_pipe)
        case "-":
            if cur_pos.x == prev_pos.x - 1:
                # we're moving left
                next_pipe = input[cur_pos.y][cur_pos.x - 1]
                next_pos = Pos(cur_pos.x - 1, cur_pos.y, next_pipe)
            else:
                # we're moving right
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                next_pos = Pos(cur_pos.x + 1, cur_pos.y, next_pipe)
        case "L":
            if cur_pos.x == prev_pos.x - 1:
                # we're moving up (from right)
                next_pipe = input[cur_pos.y - 1][cur_pos.x]
                next_pos = Pos(cur_pos.x, cur_pos.y - 1, next_pipe)
            else:
                # we're moving right (from above)
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                next_pos = Pos(cur_pos.x + 1, cur_pos.y, next_pipe)
        case "J":
            if cur_pos.x == prev_pos.x + 1:
                # we're moving up (from left)
                next_pipe = input[cur_pos.y - 1][cur_pos.x]
                next_pos = Pos(cur_pos.x, cur_pos.y - 1, next_pipe)
            else:
                # we're moving left (from above)
                next_pipe = input[cur_pos.y][cur_pos.x - 1]
                next_pos = Pos(cur_pos.x - 1, cur_pos.y, next_pipe)
        case "7":
            if cur_pos.x == prev_pos.x + 1:
                # we're moving down (from left)
                next_pipe = input[cur_pos.y + 1][cur_pos.x]
                next_pos = Pos(cur_pos.x, cur_pos.y + 1, next_pipe)
            else:
                # we're moving left (from below)
                next_pipe = input[cur_pos.y][cur_pos.x - 1]
                next_pos = Pos(cur_pos.x - 1, cur_pos.y, next_pipe)
        case "F":
            if cur_pos.x == prev_pos.x - 1:
                # we're moving down (from right)
                next_pipe = input[cur_pos.y + 1][cur_pos.x]
                next_pos = Pos(cur_pos.x, cur_pos.y + 1, next_pipe)
            else:
                # we're moving right (from below)
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                next_pos = Pos(cur_pos.x + 1, cur_pos.y, next_pipe)
        case ".":
            raise Exception(f"'.' at {cur_pos}. What? prev_pos is {prev_pos}")
        case "S":
            # check above and right and below (works for the examples in part 2 and the real input :)
            next_pipe = input[cur_pos.y - 1][cur_pos.x]
            if next_pipe in ["7", "F", "|"]:
                # above
                next_pos = Pos(cur_pos.x, cur_pos.y - 1, next_pipe)
            else:
                next_pipe = input[cur_pos.y][cur_pos.x + 1]
                if next_pipe in ["7", "J", "-"]:
                    # right
                    next_pos = Pos(cur_pos.x + 1, cur_pos.y, next_pipe)
                else:
                    # check below
                    next_pipe = input[cur_pos.y + 1][cur_pos.x]
                    if next_pipe in ["L", "J", "|"]:
                        next_pos = Pos(cur_pos.x, cur_pos.y + 1, next_pipe)

    # print(cur_pos, next_pos)

    if next_pos.pipe == "S":
        # We're back at S again
        return (None, None)

    return (next_pos, cur_pos)


def create_vertical_edge(p1, p2):
    if p1.y < p2.y:
        return (p1, p2, "V", "DOWN_DIR")
    else:
        return (p2, p1, "V", "UP_DIR")


def create_horizontal_edge(p1, p2):
    if p1.x < p2.x:
        return (p1, p2, "H", "RIGHT_DIR")
    else:
        return (p2, p1, "H", "LEFT_DIR")


def is_corner(prev_pos, next_pos):
    if next_pos.x != prev_pos.x and next_pos.y != prev_pos.y:
        # cur_pos is a corner
        return True
    return False


def create_edges(traced_positions):
    # assume S is an edge vertex (all examples + input says it is)
    edges = set()
    pos_cnt = len(traced_positions)

    # first find the first edge start on or after the start pos
    i = 0
    cur_pos = None
    prev_pos = traced_positions[0][1]
    next_pos = traced_positions[1][0]
    while not is_corner(prev_pos, next_pos):
        next_pos = traced_positions[(i + 1) % pos_cnt][0]
        (cur_pos, prev_pos) = traced_positions[i % pos_cnt]
        i += 1

    edge_start = cur_pos

    print("Edge start", edge_start)

    # then find the rest of the edges
    while i < pos_cnt + 2:
        # is cur_pos a corner?
        next_pos = traced_positions[(i + 1) % pos_cnt][0]
        # print(prev_pos, cur_pos, next_pos)
        if is_corner(prev_pos, next_pos):
            # cur_pos is a corner
            if edge_start.y != cur_pos.y:
                # vertical edge
                edges.add(create_vertical_edge(edge_start, cur_pos))
                # print("vertical edge", edge_start, cur_pos)
            else:
                edges.add(create_horizontal_edge(edge_start, cur_pos))
                # print("horizontal edge", edge_start, cur_pos)
            edge_start = cur_pos
        i += 1
        (cur_pos, prev_pos) = traced_positions[i % pos_cnt]

    return edges


def trace_positions(input):
    start_pos = find_start_pos(input)
    print("Starting at", start_pos)
    cur_pos = start_pos
    prev_pos = None
    traced_positions = []
    traced_positions_set = set()  # used to do quick lookup later
    while cur_pos is not None:
        # print(cur_pos)
        traced_positions.append((cur_pos, prev_pos))
        traced_positions_set.add((cur_pos.x, cur_pos.y))
        (cur_pos, prev_pos) = find_next_pos(cur_pos, prev_pos)

    # add the last pos as prev pos to start pos
    last_pos = traced_positions[len(traced_positions) - 1][0]
    traced_positions[0] = (start_pos, traced_positions[len(traced_positions) - 1][0])
    return (traced_positions, traced_positions_set)


def is_inside_map(pos, x_len, y_len):
    if (pos.x >= 0 and pos.x < x_len) and (pos.y >= 0 and pos.y < y_len):
        # print("Inside map")
        return True
    return False


def intersection_count(pos, max_pos, edges):
    horizontal_edges = set()
    vertical_edge_map = {}
    v_count = 0
    for edge in edges:
        if edge[2] == "V":
            if pos[1] >= edge[0].y and pos[1] <= edge[1].y:
                if pos[0] < edge[0].x and max_pos[0] > edge[0].x:
                    vertical_edge_map[edge[0]] = edge
                    vertical_edge_map[edge[1]] = edge
                    # print("pos", pos, "hit vertical edge", edge)
                    v_count += 1
        else:
            if pos[1] == edge[0].y:
                if pos[0] < edge[0].x and max_pos[0] > edge[1].x:
                    horizontal_edges.add(edge)
                    # print("pos", pos, "runs over horizontal edge", edge)

    if len(vertical_edge_map) > 0:
        if len(horizontal_edges) > 0:
            for p1, p2, type, dir in horizontal_edges:
                try:
                    vertical_edge_p1 = vertical_edge_map[p1]
                    vertical_edge_p2 = vertical_edge_map[p2]
                except KeyError:
                    print(p1)
                    print(p2)
                    print(type, dir)
                    raise
                if vertical_edge_p1[3] == vertical_edge_p2[3]:
                    # same dir on the vertical edges connected to this horizontal edge
                    # count it as one hit only
                    # example:
                    #            |
                    #         ----
                    #         |
                    # print(
                    #     pos,
                    #     "same dir on vertical edges",
                    #     vertical_edge_p1,
                    #     vertical_edge_p2,
                    # )
                    v_count -= 1

    # if v_count % 2 != 0:
    #     print(pos, "is inside")
    return v_count


def find_enclosed_ground_positions(traced_positions_set, edges, input, x_len, y_len):
    enclosed_ground_positions = set()
    for y, line in enumerate(input):
        for x, _ in enumerate(line.strip()):
            if (x, y) in traced_positions_set:
                continue
            # ray cast to a pos > all x and check how many segments we intersect
            max_pos = (x_len, y)
            if intersection_count((x, y), max_pos, edges) % 2 != 0:
                # inside
                enclosed_ground_positions.add((x, y))

    return enclosed_ground_positions


(traced_positions, traced_positions_set) = trace_positions(input)
edges = create_edges(traced_positions)
# for e in edges:
#     print("edge", e)
x_len = len(input[0].strip())
y_len = len(input)
enclosed_ground_positions = find_enclosed_ground_positions(
    traced_positions_set, edges, input, x_len, y_len
)
# for e in enclosed_ground_positions:
#     print("enclosed", e)
print(len(enclosed_ground_positions))

# 185 too low
