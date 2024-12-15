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
seconds = 100
robots: list[Robot] = read_lines("input")

# print("Initial state")
# for robot in robots:
#     print(robot)

for s in range(1, seconds + 1):
    print("Second", s)
    for robot in robots:
        robot.move(w, h)
        # print(robot)

mw = int(w / 2)
mh = int(h / 2)

q_counts = [0, 0, 0, 0]
for robot in robots:
    print(robot)
    if robot.px >= 0 and robot.px < mw:
        if robot.py >= 0 and robot.py < mh:
            # q1
            q_counts[0] += 1
        elif robot.py > mh:
            # q3
            q_counts[2] += 1
    elif robot.px > mw:
        if robot.py >= 0 and robot.py < mh:
            # q2
            q_counts[1] += 1
        elif robot.py > mh:
            # q4
            q_counts[3] += 1
# print(q_counts)
safety_factor = 1
for q_count in q_counts:
    safety_factor *= q_count
print("sf", safety_factor)
