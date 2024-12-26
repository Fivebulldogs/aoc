from collections import defaultdict
import heapq


def read_file(filename):
    byte_positions = defaultdict(set)
    byte_position_ids = {}
    byte_position_list = []
    with open(filename) as f:
        line = f.readline()
        i = 0
        while line:
            split_line = line.strip().split(",")
            x = int(split_line[0])
            y = int(split_line[1])
            byte_position_list.append((x, y))
            byte_positions[x].add(y)
            byte_position_ids[(x, y)] = i
            line = f.readline()
            i += 1
    return (byte_positions, byte_position_list, byte_position_ids)


def position_blocked(pos, byte_positions, byte_position_ids, byte_count):
    (x, y) = pos
    y_set = byte_positions.get(x)
    if y_set is not None and y in y_set and byte_position_ids[(x, y)] < byte_count:
        return True
    return False


def get_neighbors(
    pos: tuple[int, int], byte_positions: dict, byte_position_ids, byte_count, size: int
):
    (x, y) = pos
    neighbors = []

    # above
    if y > 0:
        if not position_blocked(
            (x, y - 1), byte_positions, byte_position_ids, byte_count
        ):
            neighbors.append((x, y - 1))
    # below
    if y < size - 1:
        if not position_blocked(
            (x, y + 1), byte_positions, byte_position_ids, byte_count
        ):
            neighbors.append((x, y + 1))
    # left
    if x > 0:
        if not position_blocked(
            (x - 1, y), byte_positions, byte_position_ids, byte_count
        ):
            neighbors.append((x - 1, y))
    # right
    if x < size - 1:
        if not position_blocked(
            (x + 1, y), byte_positions, byte_position_ids, byte_count
        ):
            neighbors.append((x + 1, y))

    return neighbors


# size = 7
# start_byte_count = 12
size = 71
start_byte_count = 1024

(byte_positions, byte_position_list, byte_position_ids) = read_file("input")

byte_count = start_byte_count
while True:
    # build the graph
    neighbors = defaultdict(set)
    costs = {}
    for x in range(size):
        for y in range(size):
            if position_blocked((x, y), byte_positions, byte_position_ids, byte_count):
                # blocked by a byte
                continue
            costs[(x, y)] = 1e9
            for neighbor in get_neighbors(
                (x, y), byte_positions, byte_position_ids, byte_count, size
            ):
                neighbors[(x, y)].add(neighbor)

    # traverse graph from top left to bottom right
    start = (0, 0)
    end = (size - 1, size - 1)
    costs[(0, 0)] = 0

    h = []
    heapq.heappush(h, (costs[start], start))
    visited = set()
    prev = {}
    path_found = False
    while True:
        try:
            (cost, pos) = heapq.heappop(h)
            if pos == end:
                path_found = True
                break
            if pos not in visited:
                for neighbor in neighbors.get(pos):
                    if costs[neighbor] > cost + 1:
                        costs[neighbor] = cost + 1
                        prev[neighbor] = pos
                    heapq.heappush(h, (cost + 1, neighbor))
            visited.add(pos)
        except IndexError:
            print("No path found! Byte count is", byte_count)
            breaking_pos = byte_position_list[byte_count - 1]
            print(f"Breaking position is {breaking_pos[0]},{breaking_pos[1]}")
            break

    if not path_found:
        break
    else:
        byte_count += 1
        print("Increased byte count to", byte_count)
