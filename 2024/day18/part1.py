from collections import defaultdict
import heapq


def read_file(filename, byte_count):
    byte_positions = defaultdict(set)
    with open(filename) as f:
        line = f.readline()
        i = 0
        while line and i < byte_count:
            split_line = line.strip().split(",")
            x = int(split_line[0])
            y = int(split_line[1])
            byte_positions[x].add(y)
            line = f.readline()
            i += 1
    return byte_positions


def get_neighbors(pos: tuple[int, int], byte_positions: dict, size: int):
    (x, y) = pos
    neighbors = []

    # above
    if y > 0:
        y_set = byte_positions.get(x)

        if y_set is None or y - 1 not in y_set:
            neighbors.append((x, y - 1))
    # below
    if y < size - 1:
        y_set = byte_positions.get(x)
        if y_set is None or y + 1 not in y_set:
            neighbors.append((x, y + 1))
    # left
    if x > 0:
        y_set = byte_positions.get(x - 1)
        if y_set is None or y not in y_set:
            neighbors.append((x - 1, y))
    # right
    if x < size - 1:
        y_set = byte_positions.get(x + 1)
        if y_set is None or y not in y_set:
            neighbors.append((x + 1, y))

    return neighbors


def print_map(byte_positions, path):
    for y in range(size):
        for x in range(size):
            if (x, y) in path:
                print("o", end="")
            else:
                y_set = byte_positions.get(x)
                if y_set is not None and y in y_set:
                    # blocked by a byte
                    print("#", end="")
                else:
                    print(".", end="")
        print()


size = 71
byte_count = 1024

byte_positions = read_file("input", byte_count)

# build the graph
neighbors = defaultdict(set)
costs = {}
for x in range(size):
    for y in range(size):
        y_set = byte_positions.get(x)
        if y_set is not None and y in y_set:
            # blocked by a byte
            continue
        costs[(x, y)] = 1e9
        for neighbor in get_neighbors((x, y), byte_positions, size):
            neighbors[(x, y)].add(neighbor)

# traverse graph from top left to bottom right
start = (0, 0)
end = (size - 1, size - 1)
costs[(0, 0)] = 0

h = []
heapq.heappush(h, (costs[start], start))
visited = set()
prev = {}
while True:
    try:
        (cost, pos) = heapq.heappop(h)
        if pos == end:
            print("step count", cost)
            break
        if pos not in visited:
            for neighbor in neighbors.get(pos):
                if costs[neighbor] > cost + 1:
                    costs[neighbor] = cost + 1
                    prev[neighbor] = pos
                heapq.heappush(h, (cost + 1, neighbor))
        visited.add(pos)
    except IndexError:
        break

path = set()
pos = end
while pos is not None:
    path.add(pos)
    pos = prev.get(pos)
print_map(byte_positions, path)
