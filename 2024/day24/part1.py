from collections import deque


def read_file(filename):
    wire_values = {}
    gates = {}
    with open(filename) as f:
        line = f.readline()
        while line and len(line.strip()) > 0:
            split = line.strip().split(":")
            wire_values[split[0]] = int(split[1].strip())
            line = f.readline()
        line = f.readline()

        while line and len(line.strip()) > 0:
            split0 = line.strip().split(" -> ")
            split1 = split0[0].split(" ")
            gates[split0[1]] = (split1[1], (split1[0], split1[2]))
            line = f.readline()

    return wire_values, gates


def operation(op, in1, in2):
    match op:
        case "XOR":
            return in1 ^ in2
        case "AND":
            return in1 & in2
        case "OR":
            return in1 | in2
        case _:
            assert False


(wire_values, gates) = read_file("input")

gate_q = deque()

outputs = {}
for out, gate in gates.items():
    op = gate[0]
    in1 = gate[1][0]
    in2 = gate[1][1]
    if in1 in wire_values and in2 in wire_values:
        outputs[out] = operation(op, wire_values[in1], wire_values[in2])
    else:
        gate_q.append((out, gate))

while True:
    try:
        (out, gate) = gate_q.pop()
    except IndexError:
        break
    op = gate[0]
    in1 = gate[1][0]
    in2 = gate[1][1]

    if outputs.get(in1) is not None and outputs.get(in2) is not None:
        outputs[out] = operation(op, outputs[in1], outputs[in2])
    else:
        gate_q.appendleft((out, gate))

i = 0
result = ""
while True:
    key = f"z{i:02}"
    output = outputs.get(key)
    if output is None:
        break
    result = f"{output}{result}"
    i += 1
print(result)
print(int(result, 2))
