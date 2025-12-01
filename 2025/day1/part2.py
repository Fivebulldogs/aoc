# rotations = [
#     "L68",
#     "L30",
#     "R48",
#     "L5",
#     "R60",
#     "L55",
#     "L1",
#     "L99",
#     "R14",
#     "L82"]

def read_input():
    lines = []
    with open("input.txt") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return  lines

def next_position(curr_pos, rotation):
    direction = rotation[0]
    rot_count = int(rotation[1:])
    if rotation.startswith("L"):
        next_pos = (curr_pos - rot_count) % 100
    else:
        next_pos = (curr_pos + rot_count) % 100

    full_rotations = int(rot_count / 100)
    zero_pass_count = full_rotations
    if direction == "L":
        if next_pos == 0:
            zero_pass_count += 1
        elif curr_pos != 0 and next_pos > curr_pos:
            zero_pass_count += 1
    else:
        if next_pos == 0:
            zero_pass_count += 1
        elif curr_pos != 0 and next_pos < curr_pos:
            zero_pass_count += 1

    print("next_pos", next_pos, "full_rotations", full_rotations, "zero_pass_count", zero_pass_count)

    return (next_pos, zero_pass_count)

rotations = read_input()
total_zero_pass_count = 0
curr_pos = 50
print(f"Starting at {curr_pos}")
for rotation in rotations:
    print(f"{rotation}")
    curr_pos, zero_pass_count = next_position(curr_pos, rotation)
    total_zero_pass_count += zero_pass_count
print(f"Password: {total_zero_pass_count}")
