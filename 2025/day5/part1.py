from collections import deque

def read_input():
    ranges = []
    ids = []
    with open("input") as f:
        line = f.readline()
        while line:
            if "-" in line:
                range = line.strip().split("-")
                ranges.append((range[0], range[1]))
            elif len(line) > 1:
                ids.append(int(line.strip()))
            line = f.readline()
    return (ranges, ids)

ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
ids = [1, 5,8,11,17,32]

# (ranges, ids) = read_input()
# print(ranges)
# print(ids)

def merge_ranges(r1, r2):
    r = []
    if r1[0] >= r2[0]:
        if r1[0] <= r2[1]:
            r = (r1[0], r2[1])

    return r

q = deque()
q.append(ranges[0])
while True:
    r1 = q.popleft()
    r2 = q.popleft()
    r = merge_ranges(r1, r2)