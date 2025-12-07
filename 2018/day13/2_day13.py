import sys
from functools import cmp_to_key


def read_input(filename):
    with open(filename) as f:
        rows = []
        row = f.readline()
        while row:
            rows.append(row[:-1])
            row = f.readline()
    return rows


def extract_carts(rows):
    carts = {}
    _id = 0
    for y, row in enumerate(rows):
        for x, dir in enumerate(row):
            if dir == ">" or dir == "<" or dir == "^" or dir == "v":
                carts[_id] = {"x": x, "y": y, "dir": dir, "turn_count": 0}
                _id += 1

    for (_, cart) in carts.items():
        x = cart["x"]
        y = cart["y"]
        repl = None
        if cart["dir"] == ">" or cart["dir"] == "<":
            repl = "-"
        elif cart["dir"] == "^" or cart["dir"] == "v":
            repl = "|"
        rows[y] = f"{rows[y][:x]}{repl}{rows[y][x+1:]}"
    return (rows, carts)


def print_track(tick, rows, carts):
    print(f"Tick {tick}")
    carts_print_count = 0
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if carts_print_count < len(carts):
                cart_printed = False
                for (_id, cart) in carts.items():
                    if cart["x"] == x and cart["y"] == y:
                        print(f"\033[91m{cart['dir']}", end="")
                        cart_printed = True
                        carts_print_count += 1
                        break
                if not cart_printed:
                    print(f"\033[93m{c}", end="")
            else:
                print(f"\033[93m{c}", end="")
        print()
    input("Press enter.")


def move_cart(cart_id, cart, rows, tick):
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


def get_colliding_cart_ids(tick, carts):
    colliding_cart_ids = set()
    for (_id1, cart1) in carts.items():
        for (_id2, cart2) in carts.items():
            if _id1 == _id2 or (
                _id1 in colliding_cart_ids and _id2 in colliding_cart_ids
            ):
                continue
            if cart1["x"] == cart2["x"] and cart1["y"] == cart2["y"]:
                colliding_cart_ids.add(_id1)
                colliding_cart_ids.add(_id2)
                print(
                    f"Tick {tick}: {_id1} and {_id2} collided at {cart1['x']}, {cart1['y']}. {len(carts) - len(colliding_cart_ids)} carts left."  # noqa
                )
    return colliding_cart_ids


rows = read_input(sys.argv[1])
(rows, carts) = extract_carts(rows)


def cart_cmp(cart1, cart2):
    c1 = cart1[1]
    c2 = cart2[1]
    if c1["y"] < c2["y"]:
        return -1
    elif c1["y"] > c2["y"]:
        return 1
    else:
        if c1["x"] < c2["x"]:
            return -1
        elif c1["x"] > c2["x"]:
            return 1
        else:
            return 0


tick = 1
while True:
    if tick % 500000 == 0:
        print("tick:", tick, f"({len(carts)} carts left)")
    sorted_carts = {v[0]: v[1] for v in sorted(carts.items(), key=cmp_to_key(cart_cmp))}
    # print("sorted_carts", sorted_carts)

    colliding_cart_ids = set()
    removed_cart_ids = set()
    for (_id, cart) in sorted_carts.items():
        if _id in removed_cart_ids:
            continue
        sorted_carts[_id] = move_cart(_id, cart, rows, tick)
        colliding_cart_ids = get_colliding_cart_ids(tick, sorted_carts)
        for _id in colliding_cart_ids:
            print(f"Removing cart id {_id}")
            removed_cart_ids.add(_id)

    for _id in removed_cart_ids:
        sorted_carts.pop(_id)
    carts = sorted_carts

    # print_track(tick, rows, carts)

    if len(carts) == 1:
        print("One cart left!")
        print(carts)
        break

    tick += 1

# Wrong: (You guessed 99,102.)
