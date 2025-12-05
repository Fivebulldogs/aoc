def read_input():
    ranges = []
    ids = []
    with open("input") as f:
        line = f.readline()
        while line:
            if "-" in line:
                range = line.strip().split("-")
                ranges.append((int(range[0]), int(range[1])))
            elif len(line) > 1:
                ids.append(int(line.strip()))
            line = f.readline()
    return (ranges, ids)

def get_fresh_ids(ids, ranges):
    fresh_ids = set()
    for id in ids:
        for r in ranges:
            if id >= r[0] and id <= r[1]:
                fresh_ids.add(id)
    return fresh_ids

# ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
# ids = [1, 5,8,11,17,32]

(ranges, ids) = read_input()

fresh_ids = get_fresh_ids(ids, ranges)
print(len(fresh_ids))
