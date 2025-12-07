import sys
import copy


class Point:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __lt__(self, other):
        if self.pos[1] < other.pos[1]:
            return True
        elif self.pos[1] == other.pos[1]:
            return self.pos[0] < other.pos[0]
        return False

    def __repr__(self):
        return f"{self.pos} / {self.vel}"


def read_points():
    points = []
    with open(sys.argv[1]) as f:
        line = f.readline()
        while line:
            data = line.split("> ")
            pos_data = data[0][10:].split(",")
            px = int(pos_data[0].strip())
            py = int(pos_data[1].strip())

            vel_data = data[1][10:].split(",")
            vx = int(vel_data[0].strip())
            vy = int(vel_data[1][:-2].strip())

            point = Point((px, py), (vx, vy))
            points.append(point)
            line = f.readline()
    return points


def scale_points(points, x_pos_scale, y_pos_scale):
    min_pos_x = 1e6
    max_pos_x = -1e6
    min_pos_y = 1e6
    max_pos_y = -1e6
    scaled_points = []
    for p in points:
        scaled_point = Point(
            (int(p.pos[0] / x_pos_scale), int(p.pos[1] / y_pos_scale)),
            (int(p.vel[0]), int(p.vel[1])),
        )
        scaled_points.append(scaled_point)
        if scaled_point.pos[0] < min_pos_x:
            min_pos_x = scaled_point.pos[0]
        if scaled_point.pos[0] > max_pos_x:
            max_pos_x = scaled_point.pos[0]
        if scaled_point.pos[1] < min_pos_y:
            min_pos_y = scaled_point.pos[1]
        if scaled_point.pos[1] > max_pos_y:
            max_pos_y = scaled_point.pos[1]
    offset_x = 0
    offset_y = 0
    if min_pos_x < 0:
        offset_x = -min_pos_x
    if min_pos_y < 0:
        offset_y = -min_pos_y
    return (scaled_points, offset_x, offset_y, max_pos_x, max_pos_y)


def display(points, offset_x, offset_y, max_pos_x):
    row = 0
    col = -1
    for i in range(25):
        print(i % 10, end="")
    print()
    for point in points:
        x = point.pos[0] + offset_x
        y = point.pos[1] + offset_y
        if x != col:
            # print(x, y, end="")
            if row == y:
                print(f"{'-' * (x - col - 1)}*", end="")
                col = x
            else:
                for i in range(y - row):
                    if col == 0:
                        col = -1
                    print(f"{'-' * (max_pos_x - col)}")
                    col = 0
                print(f"{'-' * (x - col)}*", end="")
                row = y
                col = x
    print(f"{'-' * (max_pos_x - col)}")


def move_points(points):
    moved_points = []
    for point in points:
        moved_point = Point(
            (
                point.pos[0] + point.vel[0],
                point.pos[1] + point.vel[1],
            ),
            (point.vel[0], point.vel[1]),
        )
        moved_points.append(moved_point)
    return moved_points


def simulate(initial_points):
    points = copy.deepcopy(initial_points)
    time = 0
    while True:
        (scaled_points, offset_x, offset_y, max_pos_x, _) = scale_points(points, 1, 1)
        # sort points so that they're printable
        # if time % 100 == 0:
        scaled_points = sorted(scaled_points)
        # print("scaled_points:", scaled_points[:4])
        # print("max_pos_x", max_pos_x)
        if max_pos_x < 200:
            display(scaled_points, offset_x, offset_y, max_pos_x + offset_x)
            print("time", time)
            input("Press a key")

        # move points
        points = move_points(points)
        # print("points after move:", points[:4])

        time += 1


initial_points = read_points()
simulate(initial_points)
