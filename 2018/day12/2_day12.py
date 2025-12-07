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


def trim_ends(state, start_pot, generation):
    trimmed_state = state

    i = 0
    start_cnt = 0
    while trimmed_state[i] == ".":
        start_cnt += 1
        i += 1

    i = len(trimmed_state) - 1
    end_cnt = 0
    while trimmed_state[i] == ".":
        end_cnt += 1
        i -= 1

    if start_cnt < 3:
        trimmed_state = "." * (3 - start_cnt) + trimmed_state
        start_pot -= 3 - start_cnt
    elif start_cnt > 3:
        trimmed_state = trimmed_state[(start_cnt - 3) :]  # noqa
        start_pot += start_cnt - 3

    if end_cnt < 3:
        trimmed_state = trimmed_state + "." * (3 - end_cnt)
    elif end_cnt > 3:
        trimmed_state = trimmed_state[(end_cnt - 3) :]  # noqa

    return (trimmed_state, start_pot)


def calc_sum(state, start_pot):
    sum = 0
    for i in range(0, len(state)):
        j = i + start_pot
        if state[i] == "#":
            sum += j
    return sum


state = initial_state
start_pot = -3
state_map = {}
generation_count = 1000000
huge_generation = 50000000000
state_found_in_map = False

for generation in range(generation_count + 1):
    if generation % 1000 == 0:
        print("generation", generation, len(state), start_pot)
    # if generation == 1000:
    #     print(state)
    #     print(start_pot)
    #     break

    # sum = calc_sum(state, start_pot)
    stored_state = state_map.get(state)
    if stored_state:
        print(
            stored_state, "found at generation", generation, "with start_pot", start_pot
        )
        offset = start_pot - generation
        print("offset:", offset)
        start_pot_at_huge_generation = huge_generation + offset
        print(f"Extrapolating to {huge_generation}:", start_pot_at_huge_generation)
        print(calc_sum(state, start_pot_at_huge_generation))
        state_found_in_map = True
        break
    else:
        state_map[state] = {"generation": generation, "start_pot": start_pot}

    if state_found_in_map:
        break

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

    (next_state, start_pot) = trim_ends(next_state, start_pot, generation + 1)
    # print("generation", generation)
    # print(state)

    state = next_state

# state = prev_state
# start_pot = prev_start_pot
# sum = 0
# for i in range(0, len(state)):
#     j = i + start_pot
#     if state[i] == "#":
#         sum += j
# print()
# print(sum)

# 6790 too high
