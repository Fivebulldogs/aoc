from collections import defaultdict
import heapq

codes = ["539A", "964A", "803A", "149A", "789A"]
num_keypad = {
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

dir_keypad = {
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


def find_path(start, end, obstacle, costs, width, height):
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
                for neighbor in get_neighbors(pos, obstacle, width, height):
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
        costs[v] = 1e9
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


def get_num_directions(start, keys, width, height):
    directions = []
    obstacle = (0, 3)
    src = start
    for key in keys:
        target = num_keypad[key]
        costs = get_costs(num_keypad)
        costs[src] = 0
        prev = find_path(src, target, obstacle, costs, width, height)
        paths = get_paths(target, src, prev)
        directions_from_path = []
        for path in paths:
            directions_from_path.append("".join(get_directions_from_path(path)))
        directions.append(directions_from_path)
        directions.append(["A"])
        src = target
    return directions


def get_dir_directions(start, keys, width, height):
    directions = []
    obstacle = (0, 0)
    src = start
    for key in keys:
        target = dir_keypad[key]
        costs = get_costs(dir_keypad)
        costs[src] = 0
        prev = find_path(src, target, obstacle, costs, width, height)
        paths = get_paths(target, src, prev)
        directions_from_path = []
        for path in paths:
            directions_from_path.append("".join(get_directions_from_path(path)))
        directions.append(directions_from_path)
        directions.append("A")
        src = target
    return directions


def get_strings_from_directions(directions):
    direction_strings = [""]
    for direction_variants in directions:
        new_direction_strings = []
        for dir_variant in direction_variants:
            for dir_str in direction_strings:
                new_direction_strings.append(f"{dir_str}{dir_variant}")
        direction_strings = new_direction_strings
    return direction_strings


sum = 0
for code in codes:
    print("code", code)
    num_code = int(code[:-1])
    print("num_code", num_code)
    num_A_pos = (2, 3)
    num_directions = get_num_directions(num_A_pos, code, 3, 4)
    num_direction_strings = get_strings_from_directions(num_directions)

    dir_A_pos = (2, 0)
    min_len_direction_str_2 = 1e9

    for num_direction_str in num_direction_strings:
        dir_directions_1 = get_dir_directions(dir_A_pos, num_direction_str, 3, 2)
        dir_direction_strings_1 = get_strings_from_directions(dir_directions_1)
        for dir_direction_str_1 in dir_direction_strings_1:
            dir_directions_2 = get_dir_directions(dir_A_pos, dir_direction_str_1, 3, 2)
            dir_direction_strings_2 = get_strings_from_directions(dir_directions_2)
            for dir_direction_str_2 in dir_direction_strings_2:
                if len(dir_direction_str_2) < min_len_direction_str_2:
                    min_len_direction_str_2 = len(dir_direction_str_2)
    term = min_len_direction_str_2 * num_code
    sum += term
print("sum", sum)
