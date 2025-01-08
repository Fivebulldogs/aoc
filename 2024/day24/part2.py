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


def get_output(wire_values, gates):
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
    return result

def set_wire_values(x, y):
    wire_values = {}
    for i, v in enumerate(reversed(f"{x:046b}")):
        wire_values[f"x{i:02}"] = int(v)
    
    for i, v in enumerate(reversed(f"{y:046b}")):
        wire_values[f"y{i:02}"] = int(v)

    return wire_values

(_, gates) = read_file("input")

def print_wire_values(wire_values):
    print("x:", end=" ")
    for i in reversed(range(46)):
        print(wire_values[f"x{i:02}"], end="")
    print()

    print("y:", end=" ")
    for i in reversed(range(46)):
        print(wire_values[f"y{i:02}"], end="")
    print()

def check_xor(gates):
    for i in range(46):
        val = pow(2, i)
        wire_values = set_wire_values(0, val)
        output = get_output(wire_values, gates)
        if int(output, 2) != pow(2, i):
            print_wire_values(wire_values)
            print("z:", output)
            print("Bad gate at bit", i)
            print("Closest gate:", gates[f"z{i:02}"])

check_xor(gates)
