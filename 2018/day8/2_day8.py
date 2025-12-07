import sys
from collections import deque


def read_file(filename):
    result = []
    with open(filename, "r") as f:
        line = f.readline()
        result = [int(x) for x in line.strip().split(" ")]
    return result


class Header:
    def __init__(self, child_nodes_qty, metadata_qty):
        self.child_nodes_qty = child_nodes_qty
        self.metadata_qty = metadata_qty


class Node:
    def __init__(self, parent, level, start_index, child_nodes_qty, metadata_qty):
        self.header = Header(child_nodes_qty, metadata_qty)
        self.metadata_entries = []
        self.level = level
        self.children = []
        self.parent = parent
        self.start_index = start_index
        self.end_index = None
        self.children_processed = 0
        self.val = 0

    def __repr__(self):
        return f"[{self.start_index} : {self.end_index}] | {' '.join([str(x) for x in self.metadata_entries])}"


def create_node(start_index, parent, level, numbers):
    child_nodes_qty = numbers[start_index]
    metadata_qty = numbers[start_index + 1]
    return Node(parent, level, start_index, child_nodes_qty, metadata_qty)


def add_metadata(node, i):
    if node.header.child_nodes_qty > 0:
        node.end_index = i + node.header.metadata_qty
    else:
        node.end_index = node.start_index + 2 + node.header.metadata_qty
    metadata_index = node.end_index - node.header.metadata_qty
    node.metadata_entries.extend(
        numbers[metadata_index : metadata_index + node.header.metadata_qty]  # noqa
    )
    if node.header.child_nodes_qty == 0:
        node.val = sum(node.metadata_entries)
        print(f"Node at {node.start_index} has val {node.val}")
    else:
        print("parent metadata entries:", node.metadata_entries)
        for j in node.metadata_entries:
            if j <= node.header.child_nodes_qty:
                # print(j, node.children[j - 1].val)
                node.val += node.children[j - 1].val
            print(f"Node at {node.start_index} has val {node.val}")
    return node.end_index


numbers = read_file(sys.argv[1])

q = deque()
print("Pushing root at 0")
curr_node = create_node(0, None, 0, numbers)
q.append(curr_node)

i = 2
try:
    while True:
        # print(f"Popping node at {i}")
        curr_node = q.pop()

        if curr_node.header.child_nodes_qty > 0:
            if curr_node.children_processed < curr_node.header.child_nodes_qty:
                # print(
                #     f"Pushing back parent node at {i}, {curr_node.children_processed} / {curr_node.header.child_nodes_qty} done."  # noqa
                # )
                q.append(curr_node)
                # print(f"Pushing child node at {i}")
                child_node = create_node(i, curr_node, curr_node.level + 1, numbers)
                q.append(child_node)
                curr_node.children.append(child_node)
                if child_node.header.child_nodes_qty > 0:
                    i += 2
            else:
                i = add_metadata(curr_node, i)
                # print(
                #     f"All children finished. Added metadata to node with start_index at {curr_node.start_index} and end_index {curr_node.end_index}"  # noqa
                # )
                if curr_node.parent:
                    curr_node.parent.children_processed += 1
                # print(f"Index is {i}")
        else:
            i = add_metadata(curr_node, i)
            # print(
            #     f"Child node done, start index {curr_node.start_index}, end index {curr_node.end_index}"
            # )
            if curr_node.parent:
                curr_node.parent.children_processed += 1
#            print(f"Index is {i}")
except IndexError:
    print(f"All done!")
