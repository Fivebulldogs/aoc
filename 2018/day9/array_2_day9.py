import sys

curr_pos = 0
circle = [0]


def read_input():
    filename = sys.argv[1]
    with open(filename) as f:
        line = f.readline().strip()
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
        pos_to_remove = curr_pos - 7
        val_to_remove = circle[pos_to_remove]
        # print("pos_to_remove", pos_to_remove)
        # print("val_to_remove", val_to_remove)
        marble_points += val_to_remove
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
        circle.pop(pos_to_remove)
        player_scores[player] += marble_points
        if player_scores[player] > highest_score:
            # print(f"HIGH SCORE: {player_scores[player]}, player: {player}")
            highest_score = player_scores[player]
            highest_score_player = player
        # print(player_scores[player])
        curr_pos = (
            pos_to_remove if pos_to_remove >= 0 else len(circle) + pos_to_remove + 1
        )
        # print("new curr_pos:", curr_pos, f"val ({circle[curr_pos]})")
    else:
        curr_pos = (curr_pos + 1) % len(circle) + 1
        circle.insert(curr_pos, current_marble)

    # print(f"[{player}]", end=" ")
    # for i, c in enumerate(circle):
    #     if i != curr_pos:
    #         print(f"  {c}  ", end="")
    #     else:
    #         print(f" ({c}) ", end="")
    # print()

    current_marble += 1
    player = max((player + 1) % (player_count + 1), 1)


print("highest_score:", highest_score)
