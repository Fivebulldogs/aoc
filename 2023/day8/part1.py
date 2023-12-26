input = None
with open("input.txt") as f:
    input = f.readlines()

# input = ["LLR\n", "\n", "AAA = (BBB, BBB)\n", "BBB = (AAA, ZZZ)\n", "ZZZ = (ZZZ, ZZZ)\n"]


def parse_input(input):
    instructions = input[0].strip()
    nodes = {}
    for line in input[2:]:
        split_line = line.split("=")
        key = split_line[0].strip()
        l_val = split_line[1].split(",")[0].strip()[1:]
        r_val = split_line[1].split(",")[1].strip()[:-1]
        nodes[key] = {"L": l_val, "R": r_val}
    return (instructions, nodes)


(instructions, nodes) = parse_input(input)
print(nodes)

instructions_len = len(instructions)
node = "AAA"
instruction_idx = 0
steps = 0
while True:
    instruction = instructions[instruction_idx]
    print("instruction", instruction)
    node = nodes[node][instruction]
    instruction_idx = (instruction_idx + 1) % instructions_len
    steps += 1
    if node == "ZZZ":
        print(steps)
        break
