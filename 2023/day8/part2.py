from functools import cache, reduce
from collections import deque
import math

input = None
with open("input.txt") as f:
    input = f.readlines()

# input = [
#     "LR\n",
#     "\n",
#     "11A = (11B, XXX)\n",
#     "11B = (XXX, 11Z)\n",
#     "11Z = (11B, XXX)\n",
#     "22A = (22B, XXX)\n",
#     "22B = (22C, 22C)\n",
#     "22C = (22Z, 22Z)\n",
#     "22Z = (22B, 22B)\n",
#     "XXX = (XXX, XXX)\n",
# ]


def parse_input(input):
    instructions = input[0].strip()
    node_map = {}
    for line in input[2:]:
        split_line = line.split("=")
        key = split_line[0].strip()
        l_val = split_line[1].split(",")[0].strip()[1:]
        r_val = split_line[1].split(",")[1].strip()[:-1]
        node_map[key] = {"L": l_val, "R": r_val}
    return (instructions, node_map)


@cache
def get_next_z_node(cur_node, instruction_idx):
    steps = 1
    while True:
        instruction = instructions[instruction_idx]
        new_node = node_map[cur_node][instruction]
        # print("cur_node", cur_node)
        # print("instruction", instruction)
        # print("new_node", new_node)
        # print()
        if new_node.endswith("Z"):
            # print("new_node", new_node, "steps", steps)
            return (new_node, steps, instruction_idx)
        cur_node = new_node
        steps += 1
        instruction_idx = (instruction_idx + 1) % len(instructions)


(instructions, node_map) = parse_input(input)
# print(node_map)

cur_nodes = deque()
for node, next_nodes in node_map.items():
    if node.endswith("A"):
        cur_nodes.appendleft((node, 0, 0))  # node, steps, index

node_count = len(cur_nodes)
steps = 0
instructions_len = len(instructions)
instruction_idx = 0
next_z_nodes = []
while True:
    try:
        cur_node = cur_nodes.pop()
    except IndexError:
        break
    (next_z_node, z_node_steps, z_node_instruction_idx) = get_next_z_node(
        cur_node[0], instruction_idx
    )
    next_z_nodes.append((next_z_node, z_node_steps, z_node_instruction_idx))
    print(cur_node, (next_z_node, z_node_steps, z_node_instruction_idx))

gcd = math.gcd(*map(lambda x: x[1], next_z_nodes))
print(gcd)

# I see by testing that the other factors are primes, here they are:
primes = map(lambda x: int(x[1] / gcd), next_z_nodes)

# This page https://www.mometrix.com/academy/greatest-common-factor/ shows how to
# calculate the LCM, least common multiplier. So we do this now:
print(gcd * reduce(lambda x, y: x * y, primes, 1))
# 23147 too low
# 63568204859 too low
