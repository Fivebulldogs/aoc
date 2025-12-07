import sys


class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


circle = Node(0)
circle.next = circle
circle.prev = circle
curr_pos = circle


def read_input():
    filename = sys.argv[1]
    linenumber = int(sys.argv[2])
    curr_linenumber = 1
    with open(filename) as f:
        line = f.readline().strip()
        while curr_linenumber < linenumber:
            line = f.readline().strip()
            curr_linenumber += 1
    return line


line = read_input()
print(line)

player_count = int(line.split(" ")[0])
last_marble_worth = int(line.split(" ")[6]) * 100
print("last_marble_worth", last_marble_worth)
# high_score = int(line.split(" ")[11])
# print("high_score", high_score)
player = 1
player_scores = {i: 0 for i in range(1, player_count + 1)}
# print(player_scores)

# print("[-]  (0)")
highest_score = -1
highest_score_player = None

for current_marble in range(1, last_marble_worth + 1):
    if current_marble % 10000 == 0:
        print(f"{current_marble} / {last_marble_worth}")
    # print("player:", player, "current_marble:", current_marble)
    if current_marble % 23 == 0:
        marble_points = current_marble
        node_to_remove = curr_pos
        tmp = curr_pos
        for steps in range(7):
            tmp = tmp.prev
        node_to_remove = tmp
        marble_points += node_to_remove.val
        # print("marble_points", marble_points)
        # if marble_points > 0:
        #     print(
        #         "current_marble:",
        #         current_marble,
        #         "points:",
        #         marble_points,
        #         "player:",
        #         player,
        #     )
        # if marble_points == last_marble_worth:
        # print(marble_points, player)
        curr_pos = node_to_remove.next
        curr_pos.prev = node_to_remove.prev
        node_to_remove.prev.next = curr_pos

        player_scores[player] += marble_points
        if player_scores[player] > highest_score:
            # print(f"HIGH SCORE: {player_scores[player]}, player: {player}")
            highest_score = player_scores[player]
            highest_score_player = player
        # print(player_scores[player])
        # print("new curr_pos:", curr_pos, f"val ({circle[curr_pos]})")
    else:
        new_node = Node(current_marble)
        before_node = curr_pos.next
        after_node = curr_pos.next.next
        before_node.next = new_node
        after_node.prev = new_node
        new_node.prev = before_node
        new_node.next = after_node
        curr_pos = new_node

    # print(f"[{player}]", end=" ")
    # tmp = circle
    # while True:
    #     if tmp.val == curr_pos.val:
    #         print(f"  ({tmp.val})  ", end="")
    #     else:
    #         print(f" {tmp.val} ", end="")
    #     tmp = tmp.next
    #     if tmp == circle:
    #         break
    # print()

    current_marble += 1
    player = max((player + 1) % (player_count + 1), 1)


print("highest_score:", highest_score)
