import random
from enum import Enum
import math

# Map number(1-52) to 52 cards
card_suit = {
    0: 'spades',
    1: 'hearts',
    2: 'diamonds',
    3: 'clubs',
}
card_rank = {
    'spades': 0,
    'hearts': 1,
    'diamonds': 2,
    'clubs': 3,
}

# For displaying character use
suit_character = {
    'spades': 0x2660,
    'hearts': 0x2665,
    'diamonds': 0x2666,
    'clubs': 0x2663
}
rank_character = {
    '11': 'J',
    '12': 'Q',
    '13': 'K',
    '1': 'A',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10'
}

# Define the weighting of each suit and each rank to be used for card comparison
card_suit_order = {
    'spades': 5,
    'hearts': 4,
    'clubs': 3,
    'diamonds': 2,
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

# full_deck = [Card(j, i) for j in ['diamonds', 'clubs', 'hearts', 'spades'] for i in range(1, 14)]
# half_deck = [Card(j, i) for j in ['diamonds', 'clubs', 'hearts', 'spades'] for i in range(8, 14)]
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

class Actions(Enum):
    FOLD = 0
    CHECK = 1
    RAISE = 2
    ALL_IN = 3
    CALL = 4


# The constants in Node class
class NodeMeta:
    C = 1
    INF = math.inf
    N_ITERATIONS = int(1e5)

# -----------------------------probability table-------------------------------

# not_call_probability[number_of_cards] =
# [weight of losing prob, weight of current highest chip / chip cap, weight of current highest chip / balance]
# use it only when cannot be guaranteed to win
not_call_probability = {
    2: [0.2, 0.5, 0.2],
    3: [0.4, 0.3, 0.2],
    4: [0.5, 0.2, 0.3],
    5: [1.0, 0, 0]
}

# not_raise_probability[number_of_cards] =
# [weight of losing prob, weight of current highest chip / chip cap, weight of current highest chip / balance]
not_raise_probability = {
    2: [0.6, 0.2, 0.2],
    3: [0.4, 0.4, 0.2],
    4: [0.6, 0.2, 0.2],
    5: [1.0, 0, 0]
}

# add_chip_amount[number_of_cards] =
# [prob that the amount = (1-losing prob)*(max_chip-highest_chip),
# if not the amount will be multiplied by the factor, show hand prob factor: result multiplied by losing prob]
add_chip_amount = {
    2: [0.2, 0.3, 0.05],
    3: [0.3, 0.4, 0.1],
    4: [0.7, 0.7, 0.4],
    5: [1.0, 1.0, 1.0]
}

# ----------------------------- mcts -------------------------------

def make_decision_using_probability(prob):
    '''
    :param prob: (prob*100)% is True, False otherwise
    :return: True or False
    '''
    if int(prob * 100) >= random.randint(1, 100):
        return True
    return False

# ----------------------------- util ------------------------------

class Debug:
    debug = 0

def debug(*msg, sep=' ', end='\n'):
    if Debug.debug == 1:
        print("[DEBUG] ", end='')
        print(*msg, sep=sep, end=end)


# -----------------------------------------------------------
TWENTY_EIGHT_CHOOSE_FIVE = 98280 # 28 CHOOSE 5
CHANCE_NODE = 'chance_node' # directory name