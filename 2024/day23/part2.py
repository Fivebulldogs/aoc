from collections import defaultdict, deque


def read_file(filename):
    with open(filename) as f:
        return f.readlines()


def add_connection(conn_pair, connection_dict):
    connection_dict[conn_pair[0]].add(conn_pair[1])
    connection_dict[conn_pair[1]].add(conn_pair[0])


connections = read_file("input")
computers = set()
connection_dict = defaultdict(set)
for connection in connections:
    conn_pair = connection.strip().split("-")
    add_connection(conn_pair, connection_dict)
    computers.add(conn_pair[0])
    computers.add(conn_pair[1])
computers = list(sorted(computers))

intersection_dict = defaultdict(int)
for i in range(len(computers)):
    for j in range(i + 1, len(computers)):
        # get the intersection between peers of computer0 and computer1
        peers0 = connection_dict.get(computers[i])
        peers1 = connection_dict.get(computers[j])
        intersection_set = {computers[i], computers[j]}
        for elem in peers0.intersection(peers1):
            intersection_set.add(elem)
        # print(",".join(sorted(intersection_set)))
        intersection_dict[",".join(sorted(intersection_set))] += 1

max_val = -1
intersection = None
for k, v in intersection_dict.items():
    if v > max_val:
        max_val = v
        intersection = k
print(intersection, max_val)
