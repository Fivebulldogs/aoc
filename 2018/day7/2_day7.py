import sys
import heapq

BASE_STEP_TIME = None
WORKER_COUNT = None


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
        self.work_time_left = ord(self.val) - ord("A") + 1 + BASE_STEP_TIME  # noqa

    def __lt__(self, other):
        if self.prio <= other.prio:
            return True

    def __repr__(self):
        return f"{self.val}: {self.work_time_left}"


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


def get_finished_nodes(nodes_processing):
    finished_nodes = []
    for i, node in enumerate(nodes_processing):
        if node.work_time_left == 0:
            finished_nodes.append((i, node))
    # sort result in alphabetical order
    return sorted(finished_nodes, key=lambda x: x[1].val)


def give_nodes_to_workers(nodes_processing, prio_heap):
    while len(nodes_processing) < WORKER_COUNT:
        try:
            curr_node = heapq.heappop(prio_heap)
            print("Popping", curr_node.val)
            nodes_processing.append(curr_node)
        except IndexError:
            # need to check if all nodes are processed
            break


def process_nodes(nodes_processing):
    print("nodes_processing:", nodes_processing)
    for node in nodes_processing:
        node.work_time_left -= 1


def traverse_tree(node_map):
    nodes_processing = []
    time_step = 0
    prio_heap = []
    pushed_vals = set()
    result = []
    while len(result) < len(node_map):
        print(f"Time: {time_step}")
        # find nodes without parents
        for val, node in node_map.items():
            if val not in pushed_vals and len(node.parents) == 0:
                print(f"{val} has no parents, pushing it")
                node.prio = ord(node.val)
                heapq.heappush(prio_heap, node)
                pushed_vals.add(val)

        give_nodes_to_workers(nodes_processing, prio_heap)
        process_nodes(nodes_processing)

        # check if any nodes are finished
        finished_node_tuples = get_finished_nodes(nodes_processing)
        print("Finished nodes:", [x[1] for x in finished_node_tuples])
        for (i, node) in finished_node_tuples:
            finished_node = nodes_processing.pop(i)
            for child_node in finished_node.children:
                child_node.parents.remove(finished_node)
            result.append(node.val)
            print("temp result:", result)

        time_step += 1

    return (result, time_step)


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


filename = sys.argv[1]
if filename.startswith("test"):
    BASE_STEP_TIME = 0
    WORKER_COUNT = 2
else:
    BASE_STEP_TIME = 60
    WORKER_COUNT = 5

(val_set, val_map) = read_file(filename)

node_map = build_tree(val_set, val_map)
(result, time_step) = traverse_tree(node_map)
validate_result(result, val_set, val_map)
print("".join(result))
print("Time:", time_step)
