import random

# Map number(1-52) to 52 cards
card_suit = {
    0: 'blade',
    1: 'heart',
    2: 'brick',
    3: 'club',
}
card_rank = {
    'blade': 0,
    'heart': 1,
    'brick': 2,
    'club': 3,
}

# Define the weighting of each suit and each rank to be used for card comparison
card_suit_order = {
    'blade': 5,
    'heart': 4,
    'club': 3,
    'brick': 2,
}
card_rank_weight = {
    1: 19,
    2: 7,
    3: 8,
    4: 9,
    5: 10,
    6: 11,
    7: 12,
    8: 13,
    9: 14,
    10: 15,
    11: 16,
    12: 17,
    13: 18,
}

# full_deck = [Card(j, i) for j in ['brick', 'club', 'heart', 'blade'] for i in range(1, 14)]
# half_deck = [Card(j, i) for j in ['brick', 'club', 'heart', 'blade'] for i in range(8, 14)]
half_deck_count = 28
# half_deck_index_map = {0: 0, 1: 1, 2: 2, 4: 3, 5: 4}

# Define the weighting for different card type to be used for determining the winner
NOPAIR = 1
ONEPAIR = 2
TWOPAIR = 3
TRIPLE = 4
STRAIGHT = 5
FLUSH = 6
FULLHOUSE = 7
QUADRUPLE = 8
STRAIGHTFLUSH = 9
card_type_map = {
    NOPAIR: 'no pair',
    ONEPAIR: 'one pair',
    TWOPAIR: 'two pair',
    TRIPLE: 'triple',
    STRAIGHT: 'straight',
    FLUSH: 'flush',
    FULLHOUSE: 'full house',
    QUADRUPLE: 'quadruple',
    STRAIGHTFLUSH: 'straight flush'
}

class Actions:
    FOLD = 0
    CHECK = 1
    RAISE = 2