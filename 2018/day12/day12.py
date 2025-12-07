import sys
import re


def read_input(filename):
    initial_state = None
    combinations = []
    with open(filename) as f:
        line = f.readline().strip()
        initial_state = f"...{line.split(': ')[1]}..."
        f.readline()
        line = f.readline().strip()
        while line:
            comb_split = line.split(" => ")
            combinations.append((comb_split[0], comb_split[1]))
            line = f.readline().strip()

    return (initial_state, combinations)


(initial_state, combinations) = read_input(sys.argv[1])
# print(initial_state)
# print(combinations)

state = initial_state
start_pot = -3
prev_state = None
for generation in range(21):
    print("generation", generation)
    print(state)
    print("start_pot", start_pot)

    result = ""
    matches = set()
    for combination in combinations:
        if combination[1] == ".":
            continue
        lookup = combination[0].replace(".", "\\.")
        matches = matches.union(
            set(
                [m.start() + start_pot + 2 for m in re.finditer(f"(?={lookup})", state)]
            )
        )
        # print(combination, matches)
    # print(sorted(matches))
    next_state = ""
    for i in range(0, len(state)):
        j = i + start_pot
        if j in sorted(matches):
            next_state = f"{next_state}#"
        else:
            next_state = f"{next_state}."

    append_start = None
    append_end = None
    i = 0
    # for i in range(0, 3):
    while i < len(next_state):
        if next_state[i] != ".":
            if i < 3:
                append_start = 3 - i
            break
        i += 1
    cnt = 0
    for i in reversed(range(len(next_state) - 3, len(next_state))):
        if next_state[i] != ".":
            append_end = 3 - cnt
            break
        cnt += 1

    if append_start:
        next_state = "." * append_start + next_state
        start_pot -= append_start
    if append_end:
        next_state = next_state + "." * append_end

    prev_state = state
    state = next_state

state = prev_state
sum = 0
for i in range(0, len(state)):
    j = i + start_pot
    if state[i] == "#":
        # print(j, end=" ")
        sum += j
print()
print(sum)

# 6790 too high
