def read_input():
    boxes = []
    with open("input") as f:
        line = f.readline()
        i = 0
        while line:
            vals = line.strip()
            boxes.append([int(v) for v in vals])
            line = f.readline()
            i += 1
    return boxes


boxes = [[162, 817, 812],
         [57, 618, 57],
         [906, 360, 560],
         [592, 479, 940],
         [352, 342, 300],
         [466, 668, 158],
         [542, 29, 236],
         [431, 825, 988],
         [739, 650, 466],
         [52, 470, 668],
         [216, 146, 977],
         [819, 987, 18],
         [117, 168, 530],
         [805, 96, 715],
         [346, 949, 466],
         [970, 615, 88],
         [941, 993, 340],
         [862, 61, 35],
         [984, 92, 344],
         [425, 690, 689]]


def dist_sqr(box1, box2):
    d_sqr = 0
    for i in range(3):
        d_sqr += (box1[i] - box2[i]) ** 2
    return d_sqr


def box_id(box):
    return hash(f"{box[0]} {box[1]} {box[2]}")


# boxes = read_input()
box_pair_list = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        d_sqr = dist_sqr(boxes[i], boxes[j])
        box_pair_list.append((boxes[i], boxes[j], d_sqr))
box_pair_list = sorted(box_pair_list, key=lambda v: v[2])
# print(box_pair_list)

circuits = []
box_to_circuit = {}
for (box0, box1) in box_pair_list:
    # for box in box_pair:
    circuit0 = box_to_circuit.get(box0)
    circuit1 = box_to_circuit.get(box1)
    if circuit0 is not None or circuit1 is not None:
        if circuit0 == circuit1:
            # boxes already in same circuit
            continue
        elif circuit0 is not None and circuit1 is None:
            # box0 is in circuit0, but box1 is not in a circuit. add box1 to circuit0
            circuit0.add(box1)
            box_to_circuit[box1] = circuit0
        elif circuit1 is not None and circuit0 is None:
            # box1 is in circuit1, but box0 is not in a circuit. add box0 to circuit1
            circuit1.add(box0)
            box_to_circuit[box0] = circuit1
    else:
        # box0 and box1 creates a new circuit
        circuits.add()
        box_to_circuit[box0] = circuit1
