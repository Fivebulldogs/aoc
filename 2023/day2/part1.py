from collections import defaultdict


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

max_color_count = {"red": 12, "green": 13, "blue": 14}

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

# for k, v in game_map.items():
#     print(k, v)

_sum = 0
for game_id, _set in game_map.items():
    # print(game_id)
    draw_ok = True
    for draw in _set:
        for color_name, _count in draw.items():
            # print(game_id, color_name, _count)
            if _count > max_color_count[color_name]:
                # print("draw not ok")
                draw_ok = False
                break
        # print()
        if not draw_ok:
            break
    if draw_ok:
        _sum += game_id
print(_sum)
