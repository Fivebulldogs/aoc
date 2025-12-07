import string


def read_file(filename):
    lines = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            a = line.strip().split(", ")
            lines.append((int(a[0]), int(a[1])))
            line = f.readline()
    return lines


def manhattan_dist(c0, c1):
    return abs(c1[0] - c0[0]) + abs(c1[1] - c0[1])


class Coord:
    def __init__(self, _id, x, y):
        self.id = _id
        self.x = x
        self.y = y


class Grid:
    def __init__(self, start_coords):
        self.coords = []
        self.grid = {}
        self.x_dim = 0
        self.y_dim = 0

        for i, start_coord in enumerate(start_coords):
            x = start_coord[0]
            y = start_coord[1]
            coord = Coord(string.ascii_letters[i], x, y)
            self.coords.append(coord)
            self.set_(x, y, coord)
            self.x_dim = x + 1 if x > self.x_dim else self.x_dim
            self.y_dim = y + 1 if y > self.y_dim else self.y_dim

    def calculate_closest_coord(self):
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                found_coord = self.get(x, y)
                if not found_coord or not found_coord.id.isnumeric():
                    closest_coord = None
                    closest_dist_sqr = 1e6
                    for i, coord in enumerate(self.coords):
                        dist_sqr = manhattan_dist((coord.x, coord.y), (x, y))
                        if dist_sqr < closest_dist_sqr:
                            closest_dist_sqr = dist_sqr
                            closest_coord = coord
                        elif dist_sqr == closest_dist_sqr:
                            closest_coord = None
                    self.set_(x, y, closest_coord)
                # break
            # break

    def get(self, x, y):
        ymap = self.grid.get(x)
        if ymap:
            return ymap.get(y, None)
        return None

    def set_(self, x, y, val):
        if self.grid.get(x):
            self.grid[x][y] = val
        else:
            self.grid[x] = {y: val}

    def __str__(self):
        s = ""
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                v = self.get(x, y)
                if v:
                    s = f"{s}{v.id}"
                else:
                    s = f"{s}{'.'}"
            s = f"{s}\n"
        return s

    def get_infinite_area_ids(self):
        infinite_area_ids = set()
        for x in [0, self.x_dim - 1]:
            for y in range(self.y_dim):
                v = self.get(x, y)
                # print(x, y, v.id if v else None)
                if v:
                    infinite_area_ids.add(v.id)
        for y in [0, self.y_dim - 1]:
            for x in range(self.x_dim):
                v = self.get(x, y)
                # print(x, y, v.id if v else None)
                if v:
                    infinite_area_ids.add(v.id)

        return infinite_area_ids

    def get_finite_largest_area(self, infinite_area_ids):
        finite_areas = {}
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                v = self.get(x, y)
                if v and v.id not in infinite_area_ids:
                    if finite_areas.get(v.id) is not None:
                        finite_areas[v.id] += 1
                    else:
                        finite_areas[v.id] = 1
        largest_area = 0
        largest_area_id = None
        for finite_area_id, area in finite_areas.items():
            if area > largest_area:
                largest_area = area
                largest_area_id = finite_area_id
        return (largest_area_id, largest_area)


coords = read_file("input.txt")
grid = Grid(coords)
# print(grid)
grid.calculate_closest_coord()
# print(grid)
infinite_area_ids = grid.get_infinite_area_ids()
# print(infinite_area_ids)
(largest_area_id, largest_area) = grid.get_finite_largest_area(infinite_area_ids)
print(largest_area_id, largest_area)
