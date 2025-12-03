import itertools

def read_input():
    ranges = []
    with open("input.txt") as f:
        line = f.readline()
        ranges = [r.strip() for r in line.split(",")]
    return ranges

# ranges = [
# "11-22",
# "95-115",
# "998-1012",
# "1188511880-1188511890",
# "222220-222224",
# "1698522-1698528",
# "446443-446449",
# "38593856-38593862",
# "565653-565659",
# "824824821-824824827",
# "2121212118-2121212124"
# ]

ranges = read_input()

invalid_ids = []
for rid, r in enumerate(ranges):
    (start, end) = r.split("-")
    print(rid)
    for v in range(int(start), int(end)+1):
        # print("v", v)
        v_substrs = []
        for i in range(1, len(end)+1):
            substrs = []
            for b in itertools.batched(str(v), i):
                substr = "".join(map(str, b))
                substrs.append(substr)
            v_substrs.append(substrs)

        for v_substr in v_substrs:
            if len(v_substr) == 2 and len(set(v_substr)) == 1:
                invalid_ids.append(int("".join(v_substr)))

invalid_id_sum = 0
for id in invalid_ids:
    invalid_id_sum += id

print(f"invalid_id_sum: {invalid_id_sum}")