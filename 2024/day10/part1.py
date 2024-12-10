from collections import deque
from dataclasses import dataclass

def read_file(filename):
    rows = []
    trailheads = set()
    with open(filename) as f:
        line = f.readline().strip()
        i = 0
        while line:
            row = []
            for j, c in enumerate(line):
                if c == "0":
                    trailheads.add((i, j))
                row.append(int(c))
            rows.append(row)
            line = f.readline().strip()
            i += 1
    # sort trailheads for easier debugging
    trailheads = sorted(trailheads)
    return (rows, trailheads)

@dataclass(frozen=True)
class Node:
    row: int
    col: int
    val: int

def get_neighbor_nodes(node, val, rows):
    row = node.row
    col = node.col
    neighbor_nodes = list()
    # up
    if row > 0 and rows[row-1][col] == val + 1:
        neighbor_nodes.append(Node(row=row-1, col=col, val=rows[row-1][col]))
    # down
    if row < len(rows) - 1 and rows[row+1][col] == val + 1:
        neighbor_nodes.append(Node(row=row+1, col=col, val=rows[row+1][col]))
    # left
    if col > 0 and rows[row][col-1] == val + 1:
        neighbor_nodes.append(Node(row=row, col=col-1, val=rows[row][col-1]))
    # right
    if col < len(rows[0]) - 1 and rows[row][col+1] == val + 1:
        neighbor_nodes.append(Node(row=row, col=col+1, val=rows[row][col+1]))
    return neighbor_nodes



def build_graph(rows, trailheads):
    q = deque()
    total_score = 0
    for th in trailheads:
        score = 0
        nodes_reached = set()
        q.append(Node(row=th[0], col=th[1], val=0))
        while True:
            try:
                node = q.pop()    
                print("popped", node.row, node.col, node.val)
                neighbors: Node = get_neighbor_nodes(node, node.val, rows)
                for neighbor in neighbors:
                    print("neighbor", neighbor)
                    if neighbor.val < 9:
                        q.append(neighbor)
                    else:
                        nodes_reached.add(neighbor)
            except IndexError:
                print("q empty for th", th)          
                score += len(nodes_reached)
                break

        print("score", score)
        total_score += score
        
    print("total_score", total_score)


(rows, trailheads) = read_file("input")
build_graph(rows, trailheads)
