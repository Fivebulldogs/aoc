def read_input():
    lines = []
    with open("input") as f:
        line = f.readline()
        i = 0
        while line:
            lines.append(line.strip())
            line = f.readline()
            i += 1
    return lines


# lines = [
#     "7,1",
#     "11,1",
#     "11,7",
#     "9,7",
#     "9,5",
#     "2,5",
#     "2,3",
#     "7,3"]

lines = read_input()

red_tiles = []
for line in lines:
    x = int(line.split(",")[0])
    y = int(line.split(",")[1])
    red_tiles.append((x, y))


def get_area(tile1, tile2):
    width = abs(tile1[0] - tile2[0]) + 1
    height = abs(tile1[1] - tile2[1]) + 1
    area = width * height
    return area


max_area = 0
max_tiles = []
for i in range(len(red_tiles)):
    for j in range(i + 1, len(red_tiles)):
        area = get_area(red_tiles[i], red_tiles[j])
        if area > max_area:
            max_area = area
            max_tiles = [red_tiles[i], red_tiles[j]]
print(max_area)
