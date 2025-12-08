from collections import defaultdict


def read_input():
    boxes = []
    with open("input") as f:
        line = f.readline()
        i = 0
        while line:
            vals = line.strip()
            boxes.append(vals)
            line = f.readline()
            i += 1
    return boxes


# boxes = ["162,817,812",
#          "57,618,57",
#          "906,360,560",
#          "592,479,940",
#          "352,342,300",
#          "466,668,158",
#          "542,29,236",
#          "431,825,988",
#          "739,650,466",
#          "52,470,668",
#          "216,146,977",
#          "819,987,18",
#          "117,168,530",
#          "805,96,715",
#          "346,949,466",
#          "970,615,88",
#          "941,993,340",
#          "862,61,35",
#          "984,92,344",
#          "425,690,689"]

def dist_sqr(box1, box2):
    box1_vals = [int(v) for v in box1.split(",")]
    box2_vals = [int(v) for v in box2.split(",")]
    d_sqr = 0
    for i in range(3):
        d_sqr += (box1_vals[i] - box2_vals[i]) ** 2
    return d_sqr


boxes = read_input()

box_pair_list = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        d_sqr = dist_sqr(boxes[i], boxes[j])
        box_pair_list.append((boxes[i], boxes[j], d_sqr))
box_pair_list = sorted(box_pair_list, key=lambda v: v[2])

circuits = defaultdict(set)
box_to_circuit = {}
circuit_idx = 0
for (i, (box0, box1, dst_sqr)) in enumerate(box_pair_list):
    (idx0, circuit0) = box_to_circuit.get(box0, (None, None))
    (idx1, circuit1) = box_to_circuit.get(box1, (None, None))
    if circuit0 is not None and circuit1 is not None:
        if idx0 != idx1:
            # boxes in different circuits. merge the circuits and clear the old ones
            new_circuit = circuit0.union(circuit1)

            circuits[circuit_idx] = new_circuit
            for box in circuit0:
                box_to_circuit[box] = (circuit_idx, new_circuit)
            for box in circuit1:
                box_to_circuit[box] = (circuit_idx, new_circuit)
            circuit_idx += 1

            del circuits[idx0]
            del circuits[idx1]
    elif circuit0 is not None and circuit1 is None:
        # box0 is in circuit0, but box1 is not in a circuit. add box1 to circuit0
        circuit0.add(box1)
        box_to_circuit[box1] = (idx0, circuit0)
    elif circuit1 is not None and circuit0 is None:
        # box1 is in circuit1, but box0 is not in a circuit. add box0 to circuit1
        circuit1.add(box0)
        box_to_circuit[box0] = (idx1, circuit1)
    else:
        # box0 and box1 creates a new circuit
        new_circuit = {box0, box1}
        box_to_circuit[box0] = (circuit_idx, new_circuit)
        box_to_circuit[box1] = (circuit_idx, new_circuit)
        circuits[circuit_idx] = new_circuit
        circuit_idx += 1

    if len(circuits) == 1:
        key = list(circuits.keys())[0]
        if len(circuits[key]) == len(boxes):
            box0_x = int(box0.split(",")[0])
            box1_x = int(box1.split(",")[0])
            print("Result:", box0_x * box1_x)
            break
