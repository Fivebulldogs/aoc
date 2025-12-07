def read_file(filename):
    with open(filename, "r") as f:
        return f.readline()


line = read_file("input.txt")

indices_removed = -1
loops = 0
last_i = 0
while indices_removed:
    indices_removed = None
    print(f"starting at {last_i}")
    for i in range(last_i, len(line) - 1):
        j = i + 1
        same_letter = line[i].upper() == line[j].upper()
        # print("same_letter", same_letter, line[i], line[j])
        if same_letter and (
            (line[i].isupper() and not line[j].isupper())
            or (not line[i].isupper() and line[j].isupper())
        ):
            indices_removed = (i, j)
            print(f"Removing {line[i]}{line[j]} at {i}-{j} {len(line)}")
            break
    if indices_removed:
        line = line[: indices_removed[0]] + line[indices_removed[1] + 1 :]
        last_i = max(0, i - 1)
    if loops % 1000 == 0:
        print(len(line))
    loops += 1
print(line)
print("Result:", len(line))

# 9203 too high
