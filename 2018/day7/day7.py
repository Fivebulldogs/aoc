import sys
import heapq


def read_file(filename):
    val_map = {}
    val_set = set()
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            data = line.strip().split(" ")
            before = data[1]
            after = data[7]
            val_set.add(before)
            val_set.add(after)
            if val_map.get(before, None) is None:
                val_map[before] = {}
            val_map[before][after] = "after"

            if val_map.get(after, None) is None:
                val_map[after] = {}
            val_map[after][before] = "before"

            line = f.readline()
    return (val_set, val_map)


class Node:
    def __init__(self, val):
        self.val = val
        self.children = set()
        self.parents = set()
        self.prio = 0

    def __lt__(self, other):
        if self.prio <= other.prio:
            return True


def build_tree(val_set, val_map):
    processed_nodes = {}
    for val in val_set:
        node = processed_nodes.get(val)
        if not node:
            node = Node(val)
        processed_nodes[val] = node

        for k, v in val_map[val].items():
            if v == "before":
                parent_node = processed_nodes.get(k)
                if not parent_node:
                    parent_node = Node(k)
                    node.parents.add(parent_node)
                    processed_nodes[k] = parent_node
                node.parents.add(parent_node)
            else:
                child_node = processed_nodes.get(k)
                if not child_node:
                    child_node = Node(k)
                    node.children.add(child_node)
                    processed_nodes[k] = child_node
                node.children.add(child_node)
    return processed_nodes


def traverse_tree(node_map):
    h = []
    pushed_vals = set()
    result = []
    while True:
        # find nodes without parents
        for val, node in node_map.items():
            if val not in pushed_vals and len(node.parents) == 0:
                print(f"{val} has no parents, pushing it")
                node.prio = ord(node.val)
                heapq.heappush(h, node)
                pushed_vals.add(val)
        try:
            curr_node = heapq.heappop(h)
            print("Popping", curr_node.val)
            result.append(curr_node.val)
            for child_node in curr_node.children:
                child_node.parents.remove(curr_node)
        except IndexError:
            break
    return result


def validate_result(result, val_set, val_map):
    assert len(result) == len(val_set)
    for i, val in enumerate(result):
        for child_val, relation in val_map[val].items():
            for j, related_val in enumerate(result):
                if related_val == child_val:
                    if relation == "before":
                        assert j < i
                    else:
                        assert j > i


(val_set, val_map) = read_file(sys.argv[1])

node_map = build_tree(val_set, val_map)
result = traverse_tree(node_map)
validate_result(result, val_set, val_map)
print("".join(result))
