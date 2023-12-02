from collections import defaultdict
from functools import reduce


def read_input():
    with open("input.txt") as f:
        lines = []
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
        return lines


input = read_input()

# input = [
#     "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
#     "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
#     "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
#     "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
#     "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
# ]

game_map = defaultdict(list)
for i, game in enumerate(input):
    (_, sets) = game.split(":")
    sets = sets.split(";")
    for _set in sets:
        color_map = {}
        _set_splits = _set.strip().split(",")
        for _set_split in _set_splits:
            (color_count, color_name) = _set_split.strip().split(" ")
            color_map[color_name] = int(color_count)
        game_map[i + 1].append(color_map)

powers = []
for _, _set in game_map.items():
    min_count = {"red": 0, "green": 0, "blue": 0}
    for draw in _set:
        for color_name, _count in draw.items():
            if _count > min_count[color_name]:
                min_count[color_name] = _count

    powers.append(reduce(lambda x, y: x * y, min_count.values()))

print(sum(powers))
