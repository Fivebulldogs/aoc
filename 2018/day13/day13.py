import sys


def read_input(filename):
    with open(filename) as f:
        rows = []
        row = f.readline()
        while row:
            rows.append(row[:-1])
            row = f.readline()
    return rows


def extract_carts(rows):
    carts = []
    for y, row in enumerate(rows):
        for x, dir in enumerate(row):
            if dir == ">" or dir == "<" or dir == "^" or dir == "v":
                carts.append({"x": x, "y": y, "dir": dir, "turn_count": 0})

    for cart in carts:
        x = cart["x"]
        y = cart["y"]
        repl = None
        if cart["dir"] == ">" or cart["dir"] == "<":
            repl = "-"
        elif cart["dir"] == "^" or cart["dir"] == "v":
            repl = "|"
        rows[y] = f"{rows[y][:x]}{repl}{rows[y][x+1:]}"
    return (rows, carts)


def print_track(rows, carts):
    carts_print_count = 0
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if carts_print_count < 2:
                cart_printed = False
                for cart in carts:
                    if cart["x"] == x and cart["y"] == y:
                        print(cart["dir"], end="")
                        cart_printed = True
                        carts_print_count += 1
                        break
                if not cart_printed:
                    print(c, end="")
            else:
                print(c, end="")
        print()


def move_cart(cart, rows):
    x = cart["x"]
    y = cart["y"]
    dir = cart["dir"]
    turn_count = cart["turn_count"]

    if dir == "<":
        x -= 1
        if rows[y][x] == "/":
            dir = "v"
        elif rows[y][x] == "\\":
            dir = "^"
        elif rows[y][x] == "+":
            if turn_count == 0:
                dir = "v"
            elif turn_count == 2:
                dir = "^"
            turn_count = (turn_count + 1) % 3
    elif dir == ">":
        x += 1
        if rows[y][x] == "/":
            dir = "^"
        elif rows[y][x] == "\\":
            dir = "v"
        elif rows[y][x] == "+":
            if turn_count == 0:
                dir = "^"
            elif turn_count == 2:
                dir = "v"
            turn_count = (turn_count + 1) % 3
    elif dir == "^":
        y -= 1
        if rows[y][x] == "/":
            dir = ">"
        elif rows[y][x] == "\\":
            dir = "<"
        elif rows[y][x] == "+":
            if turn_count == 0:
                dir = "<"
            elif turn_count == 2:
                dir = ">"
            turn_count = (turn_count + 1) % 3
    elif dir == "v":
        y += 1
        if rows[y][x] == "/":
            dir = "<"
        elif rows[y][x] == "\\":
            dir = ">"
        elif rows[y][x] == "+":
            if turn_count == 0:
                dir = ">"
            elif turn_count == 2:
                dir = "<"
            turn_count = (turn_count + 1) % 3

    return {"x": x, "y": y, "dir": dir, "turn_count": turn_count}


def get_cart_collision_pos(carts):
    cart_position_set = set()
    for cart in carts:
        if (cart["x"], cart["y"]) in cart_position_set:
            return (cart["x"], cart["y"])
        else:
            cart_position_set.add((cart["x"], cart["y"]))
    return None


rows = read_input(sys.argv[1])
(rows, carts) = extract_carts(rows)
cart_count = len(carts)
print("cart_count", cart_count)

tick = 0
while True:
    if tick % 100 == 0:
        print("tick:", tick)
    # print_track(rows, carts)
    carts_moved_count = 0
    new_carts = []
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            for i, cart in enumerate(carts):
                if cart["x"] == x and cart["y"] == y:
                    new_carts.append(move_cart(cart, rows))
                    carts_moved_count += 1
                    break
            if carts_moved_count == cart_count:
                break
        if carts_moved_count == cart_count:
            break
    carts = new_carts
    collision_pos = get_cart_collision_pos(carts)
    if collision_pos:
        print("collision_pos", collision_pos)
        break

    tick += 1
