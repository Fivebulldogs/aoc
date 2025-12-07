import string


def read_file(filename):
    with open(filename, "r") as f:
        return f.readline()


line = read_file("input.txt")


def fully_react(line):
    indices_removed = -1
    loops = 0
    last_i = 0
    while indices_removed:
        indices_removed = None
        for i in range(last_i, len(line) - 1):
            j = i + 1
            same_letter = line[i].upper() == line[j].upper()
            if same_letter and (
                (line[i].isupper() and not line[j].isupper())
                or (not line[i].isupper() and line[j].isupper())
            ):
                indices_removed = (i, j)
                break
        if indices_removed:
            line = line[: indices_removed[0]] + line[indices_removed[1] + 1 :]
            last_i = max(0, i - 1)
        # if loops % 1000 == 0:
        #    print(len(line))
        loops += 1
    return line


def remove_all_units(unit, line):
    new_line = line.replace(unit, "")
    new_line = new_line.replace(unit.upper(), "")
    return new_line


shortest = 1e6
for c in string.ascii_lowercase:
    # print(c)
    units_removed_line = remove_all_units(c, line)
    # print(units_removed_line)
    if len(units_removed_line) < len(line):
        reacted = fully_react(units_removed_line)
        if len(reacted) < shortest:
            shortest = len(reacted)
        # print(reacted, len(reacted))
print("Result:", shortest)
