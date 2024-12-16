def read_lines(filename):
    map = []
    commands = ""
    with open(filename) as f:
        line = f.readline().strip()
        while line and line != "":
            map.append(line)
            line = f.readline().strip()

        line = f.readline().strip()
        while line:
            commands = f"{commands}{line}"
            line = f.readline().strip()
    return (map, commands)


def transform_map(map):
    new_map = []
    for row in map:
        new_row = ""
        for val in row:
            if val == "O":
                new_row = f"{new_row}[]"
            elif val == "@":
                new_row = f"{new_row}@."
            else:
                new_row = f"{new_row}{val}{val}"
        new_map.append(new_row)
    return new_map


def initialize(map):
    robot = None
    boxes = list()
    walls = set()
    for i, row in enumerate(map):
        curr_box = None
        for j, val in enumerate(row):
            match val:
                case "[":
                    curr_box = []
                    curr_box.append((i, j))
                case "]":
                    curr_box.append((i, j))
                    boxes.append(curr_box)
                    curr_box = None
                case "#":
                    walls.add((i, j))
                case "@":
                    robot = (i, j)
                case ".":
                    continue
                case _:
                    print("bad val", val)
                    assert False
    return (robot, boxes, walls)


def get_first_space(command, robot, boxes, walls):
    (y, x) = robot

    while True:
        match command:
            case "^":
                y -= 1
            case ">":
                x += 1
            case "v":
                y += 1
            case "<":
                x -= 1
            case _:
                assert False

        if (y, x) in walls:
            return None
        else:
            box_found = False
            for box in boxes:
                if (y, x) == box[0] or (y, x) == box[1]:
                    box_found = True
                    break
            if box_found:
                continue
            else:
                return (y, x)


def move(command, first_space, robot, boxes):
    (ry, rx) = robot
    match command:
        case "^":
            new_robot = (ry - 1, rx)
            new_boxes = set()
            for y in range(ry - 1, first_space[0], -1):
                if (y, rx) in boxes:
                    boxes.remove((y, rx))
                    new_boxes.add((y - 1, rx))
            boxes.update(new_boxes)
        case ">":
            new_robot = (ry, rx + 1)
            new_boxes = set()
            for x in range(rx + 1, first_space[1]):
                if (ry, x) in boxes:
                    # print("Removing box at", (ry, x))
                    boxes.remove((ry, x))
                    # print("adding new box at", (ry, x + 1))
                    new_boxes.add((ry, x + 1))
            boxes.update(new_boxes)
        case "v":
            new_robot = (ry + 1, rx)
            new_boxes = set()
            for y in range(ry + 1, first_space[0]):
                if (y, rx) in boxes:
                    boxes.remove((y, rx))
                    new_boxes.add((y + 1, rx))
            boxes.update(new_boxes)
        case "<":
            new_robot = (ry, rx - 1)
            print(boxes)
            new_boxes = []
            for x in range(rx - 1, first_space[1], -1):
                box_i = None
                for i, box in enumerate(boxes):
                    if (ry, x) == box[1]:
                        new_box = [(ry, x - 1), (ry, x - 2)]
                        new_boxes.append(new_box)
                        box_i = i
                        break
                if box_i:
                    del boxes[box_i]
        case _:
            assert False
    return new_robot


def print_state(i, command, robot, boxes, walls, map):
    print("--------")
    if i >= 0 and command:
        print("Command", i, command)
    for i in range(len(map)):
        for j in range(len(map[0])):
            if robot == (i, j):
                print("@", end="")
            elif (i, j) in walls:
                print("#", end="")
            else:
                box_found = False
                for box in boxes:
                    if box[0] == (i, j):
                        print("[", end="")
                        box_found = True
                        break
                    elif box[1] == (i, j):
                        print("]", end="")
                        box_found = True
                        break
                if not box_found:
                    print(".", end="")
        print()


(map, commands) = read_lines("test_input")
map = transform_map(map)
(robot, boxes, walls) = initialize(map)

# print(boxes)
print_state(-1, None, robot, boxes, walls, map)

for i, command in enumerate(commands):
    if command in ["<" or ">"]:
        first_space = get_first_space(command, robot, boxes, walls)
    if not first_space:
        # could not move
        print_state(i, command, robot, boxes, walls, map)
        continue

    print("first_space", first_space)

    # this function will mutate the boxes set, which is ugly
    robot = move(command, first_space, robot, boxes)

    print_state(i, command, robot, boxes, walls, map)
    break

# result = 0
# for box in boxes:
#     result += 100 * box[0] + box[1]
# print("result", result)
