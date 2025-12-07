from functools import reduce


def read_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines


lines = read_file("input.txt")
s = reduce(lambda x, y: int(x) + int(y.strip()), lines)
print("Part 1: ", s)

freqs = set()
repeat_found = False
its = 0
s = 0
while not repeat_found:
    for line in lines:
        its += 1
        val = int(line.strip())
        s += val
        if s in freqs:
            repeat_found = True
            print("Part 2:", s)
            break
        freqs.add(s)
# print(its, len(lines))
