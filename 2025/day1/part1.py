# rotations = [
# "L68",
# "L30",
# "R48",
# "L5",
# "R60",
# "L55",
# "L1",
# "L99",
# "R14",
# "L82"]

def read_input():
    lines = []
    with open("input.txt") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return  lines

def next_position(curr_pos, rotation):
    rot_count = int(rotation[1:])
    if rotation.startswith("L"):
        next_pos = (curr_pos - rot_count) % 100
    else:
        next_pos = (curr_pos + rot_count) % 100
    return (next_pos, next_pos == 0)

rotations = read_input()

curr_pos = 50
zero_pos_count = 0
for rotation in rotations:
    curr_pos, is_zero_pos = next_position(curr_pos, rotation)
    print(f"{rotation} {curr_pos} {is_zero_pos}")
    if is_zero_pos:
        zero_pos_count += 1

print(f"Password: {zero_pos_count}")