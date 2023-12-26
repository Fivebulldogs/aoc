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


def get_type(hand):
    char_counts = []
    for i in range(0, 5):
        char_counts.append(hand.count(hand[i]))

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


def parse_input(input):
    hands = []
    for line in input:
        hand = {"hand": line.split()[0], "bid": int(line.split()[1])}
        hand["type"] = get_type(hand["hand"])
        hands.append(hand)

    return hands


hands = parse_input(input)

card_strengths = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


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

# 250380874 too high
