from itertools import combinations


def read_lines(filename):
    with open(filename) as f:
        return f.readlines()


lines = read_lines("input.txt")
safe_count = 0
for line in lines:
    l_split = line.split(" ")
    line_is_safe = False
    for comb in combinations(l_split, len(l_split) - 1):
        if line_is_safe:
            break
        # print("comb", comb)
        prev_dir = 0
        direction = 0
        for i, _ in enumerate(comb):
            if i == len(comb) - 1:
                safe_count += 1
                print("line is safe", line)
                line_is_safe = True
                break

            v = int(comb[i])
            next_v = int(comb[i + 1])

            if (direction > 0) and (v - next_v) > 0:
                break
            if (direction < 0) and (v - next_v) < 0:
                break

            # print(v, next_v, abs(v - next_v))
            if abs(v - next_v) < 1 or abs(v - next_v) > 3:
                break

            if direction == 0:
                if v < next_v:
                    direction = 1
                elif v > next_v:
                    direction = -1
                else:
                    break

print("safe_count", safe_count)
