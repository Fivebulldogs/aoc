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

def merge_ranges(r1, r2):
    r = []

    # completely within
    if r2[0] >= r1[0] and r2[1] <= r1[1]:
        return r1
    elif r1[0] >= r2[0] and r1[1] <= r2[1]:
        return r2

    # overlapping or having the same end
    if r2[0] >= r1[0] and r2[0] <= r1[1]:
        return (r1[0], r2[1])
    elif r2[1] >= r1[0] and r2[1] <= r1[1]:
        return (r2[0], r1[1])
    return None

def merge_all_ranges(ranges):
    while True:
        i = 0
        ranges_merged = False
        while i < len(ranges):
            j = i + 1
            while j < len(ranges):
                r = merge_ranges(ranges[i], ranges[j])
                if r != None:
                    # print("Merged", ranges[i],"and", ranges[j],"to",r)
                    ranges[i] = r
                    del ranges[j]
                    ranges_merged = True
                j += 1
            i += 1
        if not ranges_merged:
            break
    return ranges

def get_fresh_ids(ids, ranges):
    fresh_ids = set()
    for id in ids:
        for r in ranges:
            if id >= r[0] and id <= r[1]:
                fresh_ids.add(id)
    return fresh_ids

def range_sum(ranges):
    s = 0
    for r in ranges:
        diff = r[1] - r[0] + 1
        s += diff
    return s

ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
ids = [1, 5,8,11,17,32]

(ranges, ids) = read_input()

ranges = merge_all_ranges(ranges)
fresh_ids = get_fresh_ids(ids, ranges)
print(range_sum(ranges))