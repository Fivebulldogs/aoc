from dataclasses import dataclass


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    def move(self, w, h):
        new_px = self.px + self.vx
        if new_px >= w:
            self.px = new_px - w
        elif new_px < 0:
            self.px = w + new_px
        else:
            self.px = new_px

        new_py = self.py + self.vy
        if new_py >= h:
            self.py = new_py - h
        elif new_py < 0:
            self.py = h + new_py
        else:
            self.py = new_py


def read_lines(filename):
    robots = []
    with open(filename) as f:
        line = f.readline()
        while line:
            split_line = line.split(" ")

            pos = split_line[0].split("=")[1].split(",")
            px = int(pos[0])
            py = int(pos[1])
            vel = split_line[1].split("=")[1].split(",")
            vx = int(vel[0])
            vy = int(vel[1])
            robots.append(Robot(px, py, vx, vy))
            line = f.readline()
    return robots


w = 101
h = 103
# w = 11
# h = 7
seconds = 100000
robots: list[Robot] = read_lines("input")


def print_robots(positions, w, h):
    print("----------------------")
    for y in range(h):
        for x in range(w):
            if (x, y) in positions:
                print("O", end="")
            else:
                print(" ", end="")
        print()
    print("----------------------")


def count_robots_vertical(sx, ex):
    cnt = 0
    for robot in robots:
        if robot.px > sx and robot.px < ex:
            cnt += 1
    return cnt


def count_robots_horizontal(sy, ey):
    cnt = 0
    for robot in robots:
        if robot.py > sy and robot.py < ey:
            cnt += 1
    return cnt


for s in range(1, seconds + 1):
    for robot in robots:
        robot.move(w, h)

    positions = set()
    for robot in robots:
        positions.add((robot.px, robot.py))

    hcnt = count_robots_horizontal(int(h / 3), h - int(h / 3))
    hqt = hcnt / len(robots)
    vcnt = count_robots_vertical(int(w / 3), w - int(w / 3))
    vqt = vcnt / len(robots)

    if hqt > 0.5 and vqt > 0.5:
        print("Seconds", s)
        print("hqt", hcnt / len(robots))
        print("vqt", vcnt / len(robots))
        print_robots(positions, w, h)
        break
