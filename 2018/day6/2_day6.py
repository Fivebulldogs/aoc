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
        self.total_dist = 0


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

    def calculate_total_dist(self):
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                mdist_sum = 0
                for i, coord in enumerate(self.coords):
                    mdist_sum += manhattan_dist((coord.x, coord.y), (x, y))
                v = self.get(x, y)
                if not v:
                    self.set_(x, y, mdist_sum)
                else:
                    v.total_dist = mdist_sum

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
                if type(v) is not int:
                    s = f"{s}{v.id} "
                else:
                    s = f"{s}{v} "
            s = f"{s}\n"
        return s

    def get_best_region_size(self, max_total_dist):
        pos_in_region = set()
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                v = self.get(x, y)
                if type(v) is int:
                    if v < max_total_dist:
                        pos_in_region.add((x, y))
                else:
                    if v.total_dist < max_total_dist:
                        pos_in_region.add((x, y))
        return len(pos_in_region)


coords = read_file("input.txt")
grid = Grid(coords)
grid.calculate_total_dist()
# print(grid)
region_size = grid.get_best_region_size(10000)
print(region_size)
