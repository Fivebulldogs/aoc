from functools import reduce
from math import ceil, exp, floor, sqrt


input = None

def parse_input(input):
    time = int(input[0].split(":")[1].replace(" ", ""))
    record_distance = int(input[1].split(":")[1].replace(" ", ""))
    return (time, record_distance)

input = ["Time:      7  15   30\n", "Distance:  9  40  200\n"]

with open("input.txt") as f:
    input = f.readlines()

(time, record_distance) = parse_input(input)
# print(time, record_distance)
# record_beat_count = 0
# for j in range(1, time+1):
#     dist = (time - j) * j
#     if dist > record_distance:
#         record_beat_count += 1
# print(record_beat_count)
# print(sqrt(time - record_distance))
# second degree equation: j^2 - time * j + record_distance = 0
# the two roots show the interval in which the function is less or greater than the record distance
root1 = time / 2 - sqrt((time / 2) ** 2  - record_distance)
root2 = time / 2 + sqrt((time / 2) ** 2  - record_distance)
print(ceil(root1), floor(root2))
print(floor(root2) - ceil(root1) + 1)