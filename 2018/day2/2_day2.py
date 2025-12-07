import heapq


def read_file(filename):
    lines = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return lines


lines = read_file("input.txt")
q = []
for i in range(len(lines) - 1):
    for j in range(i + 1, len(lines)):
        diff = 0
        for ci in range(len(lines[0])):
            if lines[i][ci] != lines[j][ci]:
                diff += 1
        print(lines[i], lines[j], "diff:", diff)
        heapq.heappush(q, (diff, (lines[i], lines[j])))

most_like = heapq.heappop(q)
print(most_like)

for i in range(len(most_like[1][0])):
    if most_like[1][0][i] == most_like[1][1][i]:
        print(most_like[1][0][i], end="")
print()
