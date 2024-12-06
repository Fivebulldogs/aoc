from dataclasses import dataclass
import re

def read_lines(filename):
    with open(filename) as f:
        m = []
        line = f.readline()
        while line:
            m.append(list(line.strip()))
            line = f.readline()
        return m

@dataclass(frozen=True)
class Guard:
    x: int
    y: int
    dir: str

def find_guard(m):
    guard_pos = None
    for y, row in enumerate(m):
        if not guard_pos:
            match = re.search(r"\^", "".join(row))
            if match:
                guard_pos = (match.span()[0], y)
    return Guard(x=guard_pos[0], y=guard_pos[1], dir='^')

def rotate(guard, new_dir):
    return Guard(x=guard.x, y=guard.y, dir=new_dir)

def move_forward(guard, new_x, new_y):
    return Guard(x=new_x, y=new_y, dir=guard.dir)

def move(guard, m):
    match guard.dir:
        case '^':
            if guard.y > 0:
                if m[guard.y - 1][guard.x] == '#':
                    return (rotate(guard, '>'), False)
                else:
                    return (move_forward(guard, guard.x, guard.y - 1), False)
            else:
                return (None, True)
        case 'v':
            if guard.y < len(m) - 1:
                if m[guard.y + 1][guard.x] == '#':
                    return (rotate(guard, '<'), False)
                else:
                    return (move_forward(guard, guard.x, guard.y + 1), False)
            else:
                return (None, True)
        case '>':
            if guard.x < len(m[0]) - 1:
                if m[guard.y][guard.x + 1] == '#':
                    return (rotate(guard, 'v'), False)
                else:
                    return (move_forward(guard, guard.x + 1, guard.y), False)
            else:
                return (None, True)
        case '<':
            if guard.x > 0: 
                if m[guard.y][guard.x - 1] == '#':
                    return (rotate(guard, '^'), False)
                else:
                    return (move_forward(guard, guard.x - 1, guard.y), False)
            else:
                return (None, True)
        case _:
            assert(False)

def find_empty_positions(m):
    empty_positions = []
    for i, row in enumerate(m):
        for j, col in enumerate(row):
            if col == '.':
                empty_positions.append((j, i))
    return empty_positions    

orig_m = read_lines("input.txt")
empty_positions = find_empty_positions(orig_m)
start_guard = find_guard(orig_m)

obstruction_cnt = 0
for i, empty_pos in enumerate(empty_positions):
    print("empty_pos", i, "of", len(empty_positions))
    # copy m and add obstruction
    m = [l[:] for l in orig_m]
    m[empty_pos[1]][empty_pos[0]] = '#'

    prev_guard_states = set([start_guard])
    guard = start_guard
    outside_map = False
    while not outside_map:
        (guard, outside_map) = move(guard, m)
        # print(guard)
        if guard in prev_guard_states:
            # loop detected
            obstruction_cnt += 1
            break

        if not outside_map:
            prev_guard_states.add(guard)
        else:
            break
print("obstruction_cnt", obstruction_cnt)