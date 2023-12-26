from collections import defaultdict, deque

input = None
with open("input.txt") as f:
    input = f.readlines()

# input = ["0 3 6 9 12 15\n", "1 3 6 10 15 21\n", "10 13 16 21 30 45\n"]


def parse_input(input):
    lines = []
    for line in input:
        lines.append([int(c) for c in line.strip().split(" ")])
    return lines


histories = parse_input(input)


def get_diffs(history):
    all_zeros = True
    diffs = []
    for i in range(0, len(history)):
        if i > 0:
            diff = history[i] - history[i - 1]
            if diff != 0:
                all_zeros = False
            diffs.append(diff)
    return (diffs, all_zeros)


history_diffs = defaultdict(list)
for i, history in enumerate(histories):
    history_diffs[i].append(history)
    hq = deque()
    hq.appendleft(history)
    while True:
        try:
            h = hq.pop()
        except IndexError:
            raise Exception("what?")

        (diffs, all_zeros) = get_diffs(h)
        if all_zeros:
            break
        history_diffs[i].append(diffs)
        hq.appendleft(diffs)

# print(history_diffs)

sum_edge = 0
for _, hd in history_diffs.items():
    # print(hd)
    edge = 0
    for vec in reversed(hd):
        # print(vec[0], edge)
        edge = vec[0] - edge
        # print(edge)
    # print()
    sum_edge += edge
print(sum_edge)
