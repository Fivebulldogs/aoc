from enum import Enum


with open("input.txt") as f:
    input = f.readlines()

# input = ["32T3K 765\n", "T55J5 684\n", "KK677 28\n", "KTJJT 220\n", "QQQJA 483\n"]


class Type(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def get_type_without_joker(hand, char_counts):
    # normal type
    if 5 in char_counts:
        return Type.FIVE_OF_A_KIND
    elif 4 in char_counts:
        return Type.FOUR_OF_A_KIND
    elif char_counts.count(3) == 3 and char_counts.count(2) == 2:
        return Type.FULL_HOUSE
    elif char_counts.count(3) == 3 and char_counts.count(1) == 2:
        return Type.THREE_OF_A_KIND
    elif 2 in char_counts and char_counts.count(2) == 4:
        return Type.TWO_PAIR
    elif 2 in char_counts and char_counts.count(2) == 2:
        return Type.ONE_PAIR
    elif char_counts.count(1) == 5:
        return Type.HIGH_CARD
    else:
        raise Exception(f"Unable to get card type for hand {hand}: {char_counts}")


card_strengths = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def get_non_j_chars(char_count_dict):
    other_cs = []
    for c, _count in char_count_dict.items():
        if c != "J":
            other_cs.append(c)
    assert len(other_cs) > 0
    return other_cs


def get_highest_ranking_card(hand):
    lowest_index = 1e10
    lowest_index_c = None
    for c in hand:
        if c != "J" and card_strengths.index(c) < lowest_index:
            lowest_index = card_strengths.index(c)
            lowest_index_c = c
    return lowest_index_c


def remove_joker(hand, j_count, char_count_dict):
    new_hand = []
    if j_count == 5:
        # convert the 5 J:s to make the type five of a kind with highest value
        new_hand = "AAAAA"
    if j_count == 4:
        # convert the 4 J:s to make the type five of a kind
        other_cs = get_non_j_chars(char_count_dict)
        new_hand = hand.replace("J", other_cs[0])
    elif j_count == 3:
        # are the remaining two cards the same or different?
        other_cs = get_non_j_chars(char_count_dict)
        if len(char_count_dict.keys()) == 2:
            # the remaining are the same, this can be a five of a kind!
            new_hand = hand.replace("J", other_cs[0])
        else:
            # the remaining are NOT the same, pick the highest of the remaining chars
            other_cs = get_non_j_chars(char_count_dict)
            if card_strengths.index(other_cs[0]) < card_strengths.index(other_cs[1]):
                new_hand = hand.replace("J", other_cs[0])
            else:
                new_hand = hand.replace("J", other_cs[1])
    elif j_count <= 2:
        # are the remaining three the same, consist of a pair + 1 or all different?
        highest_non_j = None
        highest_non_j_count = None
        sorted_hand = sorted(char_count_dict.items(), key=lambda x: x[1], reverse=True)
        for c, _count in sorted_hand:
            if c != "J":
                highest_non_j = c
                highest_non_j_count = _count
                break

        if highest_non_j_count == 3:
            # all the three non-j cards are the same! Convert the J:s to this card to get five of a kind
            new_hand = hand.replace("J", highest_non_j)
        elif highest_non_j_count == 2:
            # two non-j cards are the same! Convert the J:s to this card to get four of a kind
            new_hand = hand.replace("J", highest_non_j)
        else:
            # all non-j cards are different. convert the j:s to the highest ranking of these to get three of a kind
            highest_ranking_card = get_highest_ranking_card(hand)
            new_hand = hand.replace("J", highest_ranking_card)
    elif j_count == 1:
        # are the remaining four the same, consist of three of a kind + 1, consist of two pairs, one pair + 2 different or all different?
        highest_non_j = None
        highest_non_j_count = None
        sorted_hand = sorted(char_count_dict.items(), key=lambda x: x[1], reverse=True)
        for c, _count in sorted_hand.items():
            if c != "J":
                highest_non_j = c
                highest_non_j_count = _count
                break

        if highest_non_j_count == 4:
            # all the four non-j cards are the same! Convert the J to this card to get five of a kind
            new_hand = hand.replace("J", highest_non_j)
        if highest_non_j_count == 3:
            # three non-j cards are the same! Convert the J to this card to get four of a kind
            new_hand = hand.replace("J", highest_non_j)
        elif highest_non_j_count == 2:
            # two non-j cards are the same! Convert the J to this card to get three of a kind
            new_hand = hand.replace("J", highest_non_j)
        else:
            # all non-j cards are different. convert the j:s to the highest ranking of these to get three of a kind
            highest_ranking_card = get_highest_ranking_card(hand)
            new_hand = hand.replace("J", highest_ranking_card)
    return new_hand


def get_type(hand):
    char_counts = []
    char_count_dict = {}
    for i in range(0, 5):
        char_counts.append(hand.count(hand[i]))
        char_count_dict[hand[i]] = hand.count(hand[i])

    j_count = char_count_dict.get("J", 0)
    if j_count > 0:
        hand = remove_joker(hand, j_count, char_count_dict)
        char_counts = []
        for i in range(0, 5):
            char_counts.append(hand.count(hand[i]))
        return get_type_without_joker(hand, char_counts)
    else:
        return get_type_without_joker(hand, char_counts)


def parse_input(input):
    hands = []
    for line in input:
        hand = {"hand": line.split()[0], "bid": int(line.split()[1])}
        hand["type"] = get_type(hand["hand"])
        hands.append(hand)

    return hands


hands = parse_input(input)


def hand_sort(hand):
    card_strength_sum = 0
    factor = 100e6
    # print(hand["hand"])
    for i, card in enumerate(hand["hand"], start=1):
        card_strength = 12 - card_strengths.index(card)
        card_strength_sum += int(factor) * card_strength
        factor /= 100
        # print(card_strength, card_strength_sum)
    return hand["type"].value * 10e9 + card_strength_sum


hands = sorted(hands, key=hand_sort)

result = 0
for i, hand in enumerate(hands, start=1):
    print(hand, i)
    result += hand["bid"] * i
print(result)
