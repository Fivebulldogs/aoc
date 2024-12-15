from dataclasses import dataclass

@dataclass(frozen=True)
class Pos:
    y: int
    x: int

@dataclass(frozen=True)
class Box:
    p1: Pos
    p2: Pos
    id: int

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
    boxes = set()
    walls = set()
    box_id = 0
    for i, row in enumerate(map):
        for j, val in enumerate(row):
            match val:
                case "[":
                    continue
                case "]":
                    boxes.add(Box(p1=Pos(i, j-1), p2=Pos(i, j), id=box_id))
                    box_id += 1
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


def get_first_space_x(command, robot, boxes, walls):
    (y, x) = robot

    while True:
        match command:
            case ">":
                x += 1
            case "<":
                x -= 1
            case _:
                assert False

        if (y, x) in walls:
            return None
        else:
            box_found = False
            for box in boxes:
                if Pos(y, x) == box.p1 or Pos(y, x) == box.p2:
                    box_found = True
                    break
            if box_found:
                continue
            else:
                return x

def get_first_space_y(command, robot, boxes, walls):
    # command is up or down
    ydir = 1 if command == "v" else -1
    ry = robot[0]
    rx = robot[1]
    boxes_to_move = set()
    x_to_move = set()
    x_to_move.add(rx)

    row = ry
    while True:
        # find all boxes that hit the x:es for the row we're currently checking
        row += ydir
        new_x_to_move = set()
        # is there a wall for any of the x:es in x_to_move?
        for x in x_to_move:
            if (row, x) in walls:
                return (None, None)
            
            # find boxes affected by x:es in x_to_move 
            for box in boxes:
                if box.p1.y == row: # box.p2.y == row too
                    if x == box.p1.x or x == box.p2.x:
                        new_x_to_move.add(box.p1.x)
                        new_x_to_move.add(box.p2.x)
                        boxes_to_move.add(box)
        if len(new_x_to_move) == 0:
            return (row, boxes_to_move)
        x_to_move = new_x_to_move            
              

def move_x(command, first_space_x, robot, boxes):
    (ry, rx) = robot

    new_robot = None
    new_boxes = set()
    boxes_to_delete = set()
    
    match command:
        case ">":
            new_robot = (ry, rx + 1)
            for x in range(rx + 1, first_space_x):
                for box in boxes:
                    if Pos(ry, x) == box.p2:
                        new_box = Box(p1=Pos(ry, x), p2=Pos(ry, x + 1), id=box.id)
                        new_boxes.add(new_box)
                        boxes_to_delete.add(box)
        case "<":
            new_robot = (ry, rx - 1)
            for x in range(rx - 1, first_space_x, -1):
                for box in boxes:
                    if Pos(ry, x) == box.p2:
                        new_box = Box(p1=Pos(ry, x - 2), p2=Pos(ry, x - 1), id=box.id)
                        new_boxes.add(new_box)
                        boxes_to_delete.add(box)
        case _:
            assert False
    for box in boxes_to_delete:
        boxes.remove(box)
        if len(boxes) > 0:
            boxes.update(new_boxes)

    return new_robot

def move_y(command, boxes_to_move, robot):
    ydir = 1 if command == "v" else -1
    boxes_to_add = set()
    if len(boxes_to_move) > 0:
        for box in boxes_to_move:
            boxes_to_add.add(Box(p1=Pos(box.p1.y + ydir, box.p1.x), 
                                 p2=Pos(box.p2.y + ydir, box.p2.x),
                                 id=box.id))

    return ((robot[0] + ydir, robot[1]), boxes_to_add)

def print_state(i, command, robot, boxes: set[Box], walls, map):
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
                    if box.p1 == Pos(i, j):
                        print("[", end="")
                        box_found = True
                        break
                    elif box.p2 == Pos(i, j):
                        print("]", end="")
                        box_found = True
                        break
                if not box_found:
                    print(".", end="")
        print()


(map, commands) = read_lines("input")
map = transform_map(map)

(robot, boxes, walls) = initialize(map)
print_state(-1, None, robot, boxes, walls, map)

for i, command in enumerate(commands):
    if command in ["<", ">"]:
        first_space_x = get_first_space_x(command, robot, boxes, walls)
        if not first_space_x:
            # could not move
            print_state(i, command, robot, boxes, walls, map)
            continue
        
        # this function will mutate the boxes set, which is ugly
        robot = move_x(command, first_space_x, robot, boxes)
    else:
        (first_space_y, boxes_to_move) = get_first_space_y(command, robot, boxes, walls)
        if not first_space_y:
            # could not move
            print_state(i, command, robot, boxes, walls, map)
            continue

        (robot, boxes_to_add) = move_y(command, boxes_to_move, robot)
        boxes = boxes.difference(boxes_to_move)
        boxes.update(boxes_to_add)

    print_state(i, command, robot, boxes, walls, map)

result = 0
for box in boxes:
    box_val = 100 * box.p1.y + box.p1.x
    result += box_val
print("result", result)
