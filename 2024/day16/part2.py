from collections import defaultdict
from dataclasses import dataclass, field
import heapq


def read_lines(filename):
    lines = []
    with open(filename) as f:
        line = f.readline().strip()
        while line:
            lines.append(line)
            line = f.readline().strip()

    return lines

def create_map(lines):
    start = None
    end = None
    map = {}
    dist = {}
    prev = defaultdict(set)
    for y, row in enumerate(lines):
        for x, val in enumerate(row):
            if val == ".":
                map[(x, y)] = val
            elif val == "S":
                start = (x, y)
                map[(x, y)] = val
            elif val == "E":
                end = (x, y)
                map[(x, y)] = val

            for dir in ["N", "S", "E", "W"]:
                dist[((x, y), dir)] = 1e9

            # start pos is special
            dist[(start, dir)] = 0

    return (map, start, end, dist, prev)

def get_neighbor_node(src_node, dest_pos):
    (xs, ys) = src_node.pos
    (xt, yt) = dest_pos
    match src_node.dir:
        case "E":
            if yt == ys:
                # horizontal
                if xt < xs:
                    # 180
                    dir = "W"
                    cost = 2000
                else:
                    # no rotation
                    dir = "E"
                    cost = 0
            else:
                # vertical
                if yt < ys:
                    # 90 ccw
                    dir = "N"
                    cost = 1000                   
                else:
                    # 90 cw
                    dir = "S"
                    cost = 1000
        case "W":
            if yt == ys:
                # horizontal
                if xt < xs:
                    # no rotation
                    dir = "W"
                    cost = 0
                else:
                    # 180
                    dir = "E"
                    cost = 2000
            else:
                # vertical
                if yt < ys:
                    # 90 cw
                    dir = "N"
                    cost = 1000
                else:
                    # 90 ccw
                    dir = "S"
                    cost = 1000
        case "S":
            if yt == ys:
                # horizontal
                if xt < xs:
                    # 90 cw
                    dir = "W"
                    cost = 1000
                else:
                    # 90 ccw
                    dir = "E"
                    cost = 1000
            else:
                # vertical
                if yt < ys:
                    # 180
                    dir = "N"
                    cost = 2000
                else:
                    # no rotation
                    dir = "S"
                    cost = 0
        case "N":
            if yt == ys:
                # horizontal
                if xt < xs:
                    # 90 ccw
                    dir = "W"
                    cost = 1000
                else:
                    # 90 cw
                    dir = "E"
                    cost = 1000
            else:
                # vertical
                if yt < ys:
                    # no rotation
                    dir = "N"
                    cost = 0
                else:
                    # 180
                    dir = "S"
                    cost = 2000

    return Node(dest_pos, dir, node.cost + cost + 1)

@dataclass(order=True)
class Node:
    pos:  tuple[int, int] = field(compare=False)
    dir:  str = field(compare=False)
    cost: int

    def __hash__(self):
        return hash((self.pos, self.dir))

def get_neighbor_nodes(node, map):
    (x, y) = node.pos
    neighbor_nodes = []
    for neighbor_pos in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
        if map.get(neighbor_pos):
            neighbor_node = get_neighbor_node(node, neighbor_pos)
            neighbor_nodes.append(neighbor_node)
    return neighbor_nodes

def find_paths(node, start_pos, prev, level):
    if node.pos == start_pos:
        return [[start_pos]]
    paths = []
    for pn in prev[(node.pos, node.dir)]:
        for path in find_paths(pn, start_pos, prev, level + 1):
            paths.append(path + [node.pos]) 
    return paths

lines = read_lines("input")
(map, start_pos, end_pos, dist, prev) = create_map(lines)

print("start", start_pos)
print("end", end_pos)

visited = set()
visited.add((start_pos, "E"))

heap = []
heapq.heappush(heap, Node(start_pos, "E", 0))

best_paths_tiles = set()

while True:
    try:
        node = heapq.heappop(heap)

        if node.pos == end_pos:
            print("cheapest path:", node.cost, dist[(node.pos, node.dir)])
            for path in find_paths(node, start_pos, prev, 0):
                best_paths_tiles.update(path)
            print("best_paths_tiles", len(best_paths_tiles))
            break

        for neighbor_node in get_neighbor_nodes(node, map):
            if dist[(neighbor_node.pos, neighbor_node.dir)] > neighbor_node.cost:
                dist[(neighbor_node.pos, neighbor_node.dir)] = neighbor_node.cost
                prev[(neighbor_node.pos, neighbor_node.dir)] = {node}
            elif dist[(neighbor_node.pos, neighbor_node.dir)] == neighbor_node.cost:
                prev[(neighbor_node.pos, neighbor_node.dir)].add(node)

            if (neighbor_node.pos, neighbor_node.dir) not in visited:
                heapq.heappush(heap, neighbor_node)
                
        visited.add((node.pos, node.dir))
    except IndexError:
        print("no more nodes")
        break
