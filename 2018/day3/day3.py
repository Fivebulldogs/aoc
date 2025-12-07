def read_file(filename):
    lines = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
    return lines


def parse_lines(lines):
    claims = []
    for line in lines:
        id_data = line.split(" @ ")
        offset_area = id_data[1].split(": ")
        x_y = offset_area[0].split(",")
        width_height = offset_area[1].split("x")
        claims.append(
            {
                "id": id_data[0],
                "x": int(x_y[0]),
                "y": int(x_y[1]),
                "width": int(width_height[0]),
                "height": int(width_height[1]),
            }
        )
    return claims


def contains(start_a, end_a, start_b, end_b):
    # print(f"{start_a} <= {start_b} and {end_a} >= {end_b}!")
    if start_a <= start_b and end_a >= end_b:
        return True
    return False


lines = read_file("input.txt")
claims = parse_lines(lines)
overlap_map = {}
for i in range(len(claims)):
    start_i = (claims[i]["x"], claims[i]["y"])
    end_i = (
        claims[i]["x"] + claims[i]["width"] - 1,
        claims[i]["y"] + claims[i]["height"] - 1,
    )
    for j in range(i + 1, len(claims)):
        # print("i:", claims[i])
        # print("j:", claims[j])
        start_j = (claims[j]["x"], claims[j]["y"])
        end_j = (
            claims[j]["x"] + claims[j]["width"] - 1,
            claims[j]["y"] + claims[j]["height"] - 1,
        )
        # print(f"i: {i}, j: {j}!")
        overlap = [None, None]
        for dim in range(2):
            if contains(start_i[dim], end_i[dim], start_j[dim], end_j[dim]):
                # overlap[dim] = end_i[dim] - start_i[dim] - (end_j[dim] - start_j[dim])
                overlap[dim] = (start_j[dim], end_j[dim])
                # print(f"i[{dim}] contains j: {overlap[dim]}")
            elif contains(start_j[dim], end_j[dim], start_i[dim], end_i[dim]):
                # overlap[dim] = end_j[dim] - start_j[dim] - (end_i[dim] - start_i[dim])
                overlap[dim] = (start_i[dim], end_i[dim])
                # print(f"j[{dim}] contains i: {overlap[dim]}")
            elif start_j[dim] >= start_i[dim] and start_j[dim] <= end_i[dim]:
                # print(f"j starts in i ({dim})")
                # overlap[dim] = end_i[dim] - start_j[dim] + 1
                overlap[dim] = (start_j[dim], end_i[dim])
            elif start_i[dim] >= start_j[dim] and start_i[dim] <= end_j[dim]:
                # print(f"i starts in j ({dim})")
                # overlap[dim] = end_j[dim] - start_i[dim] + 1
                overlap[dim] = (start_i[dim], end_j[dim])
        if None not in overlap:
            for dim in range(2):
                for x in range(overlap[0][0], overlap[0][1] + 1):
                    for y in range(overlap[1][0], overlap[1][1] + 1):
                        if not overlap_map.get(x):
                            overlap_map[x] = {y: 1}
                        else:
                            overlap_map[x][y] = 1
            # print(f"i: {i} ({start_i[0]},{start_i[1]}) / ({end_i[0]},{end_i[1]})")
            # print(f"j: {j} ({start_j[0]},{start_j[1]}) / ({end_j[0]},{end_j[1]})")
total_overlap = 0
for x, row in overlap_map.items():
    for y, v in row.items():
        # print(x, y, v)
        total_overlap += 1

print("total_overlap:", total_overlap)
# 203771, 137408 too high
# 992 too low
