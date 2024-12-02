def read_lines(filename):
    with open(filename) as f:
        return f.readlines()

lines = read_lines("input.txt")
safe_count = 0
for line in lines:
    l_split = line.split(" ")
    prev_dir = 0
    direction = 0
    for i, _ in enumerate(l_split):
        if i == len(l_split) - 1:
            safe_count += 1
            print("line is safe", line)
            break
        
        v = int(l_split[i])
        next_v = int(l_split[i+1])

        if (direction > 0) and (v - next_v) > 0:
            break
        if (direction < 0) and (v - next_v) < 0:
            break
        
        print(v, next_v, abs(v - next_v))
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

# 415 too high