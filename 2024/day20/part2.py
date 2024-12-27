from collections import defaultdict
import heapq


def read_file(filename):
    obstacles = defaultdict(list)
    costs = {}
    start = None
    end = None
    with open(filename) as f:
        line = f.readline()
        width = len(line.strip())
        y = 0
        while line:
            for x, v in enumerate(line.strip()):
                if v == "#":
                    obstacles[x].append(y)
                elif v == "S":
                    start = (x, y)
                    costs[(x, y)] = 0
                elif v == "E":
                    end = (x, y)
                    costs[(x, y)] = 1e9
                else:
                    costs[(x, y)] = 1e9
            line = f.readline()
            y += 1
    return (start, end, obstacles, costs, width, y)


def get_neighbors(
    pos: tuple[int, int],
    obstacles: dict,
    obstacle_to_remove: tuple[int, int],
    width: int,
    height: int,
):
    (x, y) = pos
    neighbors = []

    # above
    if y > 0:
        if (x, y - 1) == obstacle_to_remove:
            neighbors.append((x, y - 1))
        else:
            y_set = obstacles.get(x)
            if y_set is None or y - 1 not in y_set:
                neighbors.append((x, y - 1))
    # below
    if y < height - 1:
        if (x, y + 1) == obstacle_to_remove:
            neighbors.append((x, y + 1))
        else:
            y_set = obstacles.get(x)
            if y_set is None or y + 1 not in y_set:
                neighbors.append((x, y + 1))
    # left
    if x > 0:
        if (x - 1, y) == obstacle_to_remove:
            neighbors.append((x - 1, y))
        else:
            y_set = obstacles.get(x - 1)
            if y_set is None or y not in y_set:
                neighbors.append((x - 1, y))
    # right
    if x < width - 1:
        if (x + 1, y) == obstacle_to_remove:
            neighbors.append((x + 1, y))
        else:
            y_set = obstacles.get(x + 1)
            if y_set is None or y not in y_set:
                neighbors.append((x + 1, y))

    return neighbors


def find_path(start, end, obstacles, obstacle_to_remove, costs, width, height):
    visited = set()

    h = []
    heapq.heappush(h, (0, start))
    prev = {}

    while True:
        try:
            (cost, pos) = heapq.heappop(h)
            if pos == end:
                break
            if pos not in visited:
                for neighbor in get_neighbors(
                    pos, obstacles, obstacle_to_remove, width, height
                ):
                    if costs[neighbor] > cost + 1:
                        costs[neighbor] = cost + 1
                        prev[neighbor] = pos
                    heapq.heappush(h, (cost + 1, neighbor))
                visited.add(pos)
        except IndexError:
            pass
    return prev


def get_path(start, end, prev: dict):
    path = []
    pos = end
    while pos and pos != start:
        path.append(pos)
        pos = prev.get(pos)
    path.append(start)
    return [v for v in reversed(path)]


def get_nearby_obstacles(
    pos: tuple[int, int], obstacles: dict, width: int, height: int
):
    nearby_obstacles = []

    # above
    x = pos[0]
    y_set = obstacles.get(x)
    y = pos[1]
    while y > 0:
        if y_set is not None and y - 1 in y_set:
            nearby_obstacles.append((x, y - 1))
        y -= 1

    # below
    x = pos[0]
    y = pos[1]
    y_set = obstacles.get(x)
    while y < height - 1:
        if y_set is not None and y + 1 in y_set:
            nearby_obstacles.append((x, y + 1))
        y += 1

    # left
    x = pos[0]
    y = pos[1]
    while x > 0:
        y_set = obstacles.get(x - 1)
        if y_set is not None and y in y_set:
            nearby_obstacles.append((x - 1, y))
        x -= 1

    # right
    x = pos[0]
    y = pos[1]
    while x < width - 1:
        y_set = obstacles.get(x + 1)
        if y_set is not None and y in y_set:
            nearby_obstacles.append((x + 1, y))
        x += 1

    return nearby_obstacles


def get_costs(costs, obstacle_to_remove):
    new_costs = {}
    for k, _ in costs.items():
        new_costs[k] = 1e9
    new_costs[obstacle_to_remove] = 1e9
    return new_costs


(start, end, obstacles, original_costs, width, height) = read_file("input")
prev = find_path(start, end, obstacles, None, original_costs, width, height)
original_path = get_path(start, end, prev)
original_time = len(original_path) - 1

cheats = defaultdict(int)
visited_obstacles = set()
for i, pos in enumerate(original_path):
    if i % 100 == 0:
        print(f"At path pos {i+1} of {len(original_path)}")
    for j in range(i + 1, len(original_path)):
        pos_ahead = original_path[j]
        diff = (abs(pos_ahead[0] - pos[0]), abs(pos_ahead[1] - pos[1]))
        cheat_dist = diff[0] + diff[1]
        if cheat_dist <= 20:
            pos_path_dist = len(original_path[:i])
            pos_ahead_path_dist = len(original_path[:j])
            original_path_dist = len(original_path[i:]) - len(original_path[j:])
            if cheat_dist < original_path_dist:
                cheat_path_len = original_time - (original_path_dist - cheat_dist)
                cheats[cheat_path_len] += 1

cheat_count_at_least_100 = 0
time_saved = {original_time - time: cnt for time, cnt in cheats.items()}
for k, v in sorted(time_saved.items()):
    if k >= 100:
        cheat_count_at_least_100 += v
        print(f"{v} cheats save {k} picoseconds.")
print("cheat_count_at_least_100", cheat_count_at_least_100)
