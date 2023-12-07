# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import Counter

input_value = open("input.txt", "r").read()
lines = input_value.split("\n")

hand_bids = [x.split() for x in lines]
hand_bids = [(x[0], int(x[1])) for x in hand_bids]

# cards = "23456789TJQKA"
cards = "J23456789TQKA"


def score_tiebreak(hand):
    total = 0
    multiplier = len(cards) ** len(hand)
    for card in hand:
        total += cards.index(card) * multiplier
        multiplier /= len(cards)
    return round(total)


def score(hand):
    counter = Counter(hand)
    # This is the really devilish bit...
    count_j = counter["J"]
    del counter["J"]
    counts = sorted(counter.values(), reverse=True)
    # Five of a kind:
    if len(counts) == 0 or count_j >= (5 - counts[0]):
        return (7, score_tiebreak(hand))
    # Four of a kind:
    elif count_j >= (4 - counts[0]):
        return (6, score_tiebreak(hand))
    # Full house:
    elif count_j >= (3 - counts[0]) + (2 - counts[1]):
        return (5, score_tiebreak(hand))
    # Three of a kind:
    elif count_j >= (3 - counts[0]):
        return (4, score_tiebreak(hand))
    # Two pair:
    elif count_j >= (2 - counts[0]) + (2 - counts[1]):
        return (3, score_tiebreak(hand))
    # One pair:
    elif count_j >= (2 - counts[0]):
        return (2, score_tiebreak(hand))
    else:
        return (1, score_tiebreak(hand))


hand_bids = sorted(hand_bids, key=lambda hand_bid: score(hand_bid[0]))
print(sum(hand_bids[i][1] * (i + 1) for i in range(len(hand_bids))))
