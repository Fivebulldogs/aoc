from functools import reduce


input = None

def parse_input(input):
    vals = [[],[]]
    for i, line in enumerate(input):
        for v in line.split():
            if v.isnumeric():
                vals[i].append(int(v))
    times = vals[0]
    record_distances = vals[1]
    return (times, record_distances)

input = ["Time:      7  15   30\n", "Distance:  9  40  200\n"]

with open("input.txt") as f:
    input = f.readlines()

(times, record_distances) = parse_input(input)

record_beat_counts = []
for i, time in enumerate(times):
    record_beat_counts.append(0)
    for j in range(1, time+1):
        speed = j
        dist = (time - j) * speed
        # print(speed, dist)
        # print(dist, record_distances[i])
        if dist > record_distances[i]:
            record_beat_counts[i] += 1
    # print(record_beat_counts)
    # break

print(reduce(lambda x, y: x * y, record_beat_counts))