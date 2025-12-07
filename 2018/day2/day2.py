def read_file(filename):
    lines = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return lines


def count_chars(s):
    d = {}
    for c in s:
        if d.get(c):
            d[c] += 1
        else:
            d[c] = 1
    return d


def count_repeats(s):
    d = count_chars(s)
    # print(d)
    two_repeats = False
    three_repeats = False
    for k, v in d.items():
        if v == 2:
            two_repeats = True
        if v == 3:
            three_repeats = True
        if two_repeats and three_repeats:
            break

    return (two_repeats, three_repeats)


lines = read_file("input.txt")

two_repeats_count = 0
three_repeats_count = 0
for line in lines:
    # print(line)
    (two_repeats, three_repeats) = count_repeats(line)
    two_repeats_count = two_repeats_count + 1 if two_repeats else two_repeats_count
    three_repeats_count = (
        three_repeats_count + 1 if three_repeats else three_repeats_count
    )
print("Result part 1:", two_repeats_count * three_repeats_count)
