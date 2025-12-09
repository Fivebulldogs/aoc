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


lines = [
    "7,1",
    "11,1",
    "11,7",
    "9,7",
    "9,5",
    "2,5",
    "2,3",
    "7,3"]

# lines = read_input()

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


def get_edges(red_tiles):
    edges = []
    for i in range(len(red_tiles)):
        if i < len(red_tiles) - 1:
            edges.append((red_tiles[i], red_tiles[i + 1]))
        else:
            edges.append((red_tiles[i], red_tiles[0]))
    return edges


def edges_intersect_area(tile1, tile2, edges):
    min_x = min(tile1[0], tile2[0])
    min_y = min(tile1[1], tile2[1])
    max_x = max(tile1[0], tile2[0])
    max_y = max(tile1[1], tile2[1])
    for edge in edges:
        # raytrace instead!
        if edge[0][0] == edge[1][0]:
            # vertical edge
            x = edge[0][0]
            min_edge_point_y = min(edge[0][1], edge[1][1])
            max_edge_point_y = max(edge[0][1], edge[1][1])
            for y in range(min_edge_point_y, max_edge_point_y + 1):
                if min_y < y < max_y:
                    return True
        else:
            # horizontal edge
            y = edge[0][1]
            min_edge_point_x = min(edge[0][0], edge[1][0])
            max_edge_point_x = max(edge[0][0], edge[1][0])
            for x in range(min_edge_point_x, max_edge_point_x + 1):
                if min_x < x < max_x:
                    print("Point", x, y, "intersects")
                    return True
    return False


edges = get_edges(red_tiles)

max_area = 0
max_tiles = []
for i in range(len(red_tiles)):
    for j in range(i + 1, len(red_tiles)):
        print("--")
        print(red_tiles[i], red_tiles[j])
        if not edges_intersect_area(red_tiles[i], red_tiles[j], edges):
            area = get_area(red_tiles[i], red_tiles[j])
            print("area", area)
            if area > max_area:
                max_area = area
                max_tiles = [red_tiles[i], red_tiles[j]]
print(max_area)
