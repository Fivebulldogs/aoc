from collections import defaultdict


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

# print(connection_dict)
three_interconnected_computers = set()
for computer in computers:
    peers = connection_dict.get(computer)
    for peer in peers:
        peers_of_peer = connection_dict.get(peer)
        for peer_of_peer in peers_of_peer:
            if peer_of_peer is computer:
                continue
            if peer_of_peer in peers:
                three_interconnected_computers.add(
                    tuple(sorted((computer, peer, peer_of_peer)))
                )

sum = 0
for triple in three_interconnected_computers:
    for computer in triple:
        if computer.startswith("t"):
            sum += 1
            break
print("sum", sum)
