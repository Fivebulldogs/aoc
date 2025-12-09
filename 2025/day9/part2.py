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

def segment_intersects_rectangle(tile1, tile2):
    sorted_tiles_x = sorted((tile1, tile2), key=lambda v: v[0])
    sorted_tiles_y = sorted((tile1, tile2), key=lambda v: v[1])
    for i in range(len(red_tiles)):
        next_tile = red_tiles[(i+1) % len(red_tiles)]
        segment_x = sorted((red_tiles[i], next_tile), key=lambda v: v[0])
        segment_y = sorted((red_tiles[i], next_tile), key=lambda v: v[1])

        if red_tiles[i][0] == next_tile[0]:
            # vertical segment intersects?
            # check if segment is completely outside rectangle in y dim
            if (segment_y[0][1] <= sorted_tiles_y[0][1] and segment_y[1][1] <= sorted_tiles_y[0][1]) or \
               (segment_y[0][1] >= sorted_tiles_y[1][1] and segment_y[1][1] >= sorted_tiles_y[1][1]):
                    continue
            # check if segment is inside rectangle in x dim
            if segment_x[0][0] > sorted_tiles_x[0][0] and segment_x[1][0] < sorted_tiles_x[1][0]:
                return True
        else:
            # horizontal segment intersects?
            # check if segment is completely outside rectangle in x dim
            if (segment_x[0][0] <= sorted_tiles_x[0][0] and segment_x[1][0] <= sorted_tiles_x[0][0]) or \
               (segment_x[0][0] >= sorted_tiles_x[1][0] and segment_x[1][0] >= sorted_tiles_x[1][0]):
                    continue
            # check if segment is inside rectangle in y dim
            if segment_y[0][1] > sorted_tiles_y[0][1] and segment_y[1][1] < sorted_tiles_y[1][1]:
                return True
    return False

# sort all red tiles on x and y
red_sorted_x = sorted(red_tiles, key=lambda red_tile: red_tile[0])
x_sort_map = {red_tile: i for i, red_tile in enumerate(red_sorted_x)}

# for each red tile pair (double for), we need to quickly find if there are any other red tiles "inside" their rectangle
max_area = 0
max_tiles = []
for i in range(len(red_tiles)):
    if i % 10 == 0:
        print(f"Tile {i+1} of {len(red_tiles)}")
    for j in range(i+1, len(red_tiles)):
        if segment_intersects_rectangle(red_tiles[i], red_tiles[j]):
            continue

        area = get_area(red_tiles[i], red_tiles[j])  
        if area > max_area:
            max_area = area
            max_tiles = [red_tiles[i], red_tiles[j]]
            
print(max_area)
print(max_tiles)
