from collections import defaultdict
from functools import cache
import heapq

robot_count = 25

codes = ["539A", "964A", "803A", "149A", "789A"]
num_key_to_pos = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

dir_key_to_pos = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}


def get_neighbors(pos, obstacle, width, height):
    (x, y) = pos
    neighbors = []

    # above
    if y > 0 and (x, y - 1) != obstacle:
        neighbors.append((x, y - 1))
    # below
    if y < height - 1 and (x, y + 1) != obstacle:
        neighbors.append((x, y + 1))

    # left
    if x > 0 and (x - 1, y) != obstacle:
        neighbors.append((x - 1, y))

    # right
    if x < width - 1 and (x + 1, y) != obstacle:
        neighbors.append((x + 1, y))

    return neighbors


def find_path(start, end, costs, keypad):
    visited = set()

    h = []
    heapq.heappush(h, (0, start))
    prev = defaultdict(set)

    while True:
        try:
            (cost, pos) = heapq.heappop(h)
            if pos == end:
                break
            if pos not in visited:
                for neighbor in get_neighbors(
                    pos, keypad["obstacle"], keypad["width"], keypad["height"]
                ):
                    if costs[neighbor] > cost + 1:
                        costs[neighbor] = cost + 1
                        prev[neighbor] = {pos}
                    elif costs[neighbor] == cost + 1:
                        prev[neighbor].add(pos)
                    heapq.heappush(h, (cost + 1, neighbor))
                visited.add(pos)
        except IndexError:
            pass
    return prev


def get_paths(pos, start, prev: dict):
    if pos == start:
        return [[pos]]
    paths = []
    for prev_pos in prev[pos]:
        for path in get_paths(prev_pos, start, prev):
            paths.append(path + [pos])
    return paths


def get_costs(keypad: dict):
    costs = {}
    for v in keypad.values():
        costs[v] = 1e15
    return costs


def get_directions_from_path(path):
    directions = []
    for i, pos in enumerate(path):
        if i < len(path) - 1:
            next_pos = path[i + 1]
            if next_pos[0] < pos[0]:
                directions.append("<")
            elif next_pos[0] > pos[0]:
                directions.append(">")
            elif next_pos[1] > pos[1]:
                directions.append("v")
            else:
                directions.append("^")
    return directions


@cache
def get_last_robot_key_count(src_key, target_key, level):
    keypad_type = {
        "num": {
            "obstacle": (0, 3),
            "key_to_pos": num_key_to_pos,
            "width": 3,
            "height": 4,
        },
        "dir": {
            "obstacle": (0, 0),
            "key_to_pos": dir_key_to_pos,
            "width": 3,
            "height": 2,
        },
    }

    if level == 0:
        keypad = keypad_type["num"]
    elif level == robot_count + 1:
        return 1
    else:
        keypad = keypad_type["dir"]

    # directions_list = []
    src_pos = keypad["key_to_pos"][src_key]
    target_pos = keypad["key_to_pos"][target_key]
    costs = get_costs(keypad["key_to_pos"])
    costs[src_pos] = 0
    prev = find_path(src_pos, target_pos, costs, keypad)
    paths = get_paths(target_pos, src_pos, prev)
    min_path_count = 1e15
    for path_idx, path in enumerate(paths):
        s = "".join(get_directions_from_path(path))
        sub_src_key = "A"
        count = 0
        for key in f"{s}A":
            count += get_last_robot_key_count(sub_src_key, key, level + 1)
            sub_src_key = key

        if count < min_path_count:
            min_path_count = count

    return min_path_count


total_sum = 0
tot_min_last_directions_count = 0

for code in codes:
    print("code", code)
    min_last_directions_count = 1e15
    num_code = int(code[:-1])
    code_src_key = "A"
    sum = 0
    for code_key in code:
        last_robot_key_count = get_last_robot_key_count(code_src_key, code_key, 0)
        sum += last_robot_key_count
        code_src_key = code_key
    term = sum * num_code
    total_sum += term

print("total_sum", total_sum)
