from constants import *


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def same_suit(self, card):
        return self.suit == card.suit

    def same_rank(self, card):
        return self.rank == card.rank

    def __eq__(self, other):
        return self.same_rank(other) and self.same_suit(other)

    def __lt__(self, other):
        if card_rank_weight[self.rank] < card_rank_weight[other.rank]:
            return True
        elif self.rank == other.rank:
            return card_suit_order[self.suit] < card_suit_order[other.suit]
        return False

    def __hash__(self):
        return hash(self.suit) + hash(self.rank)

    def __str__(self):
        return chr(suit_character[self.suit]) + (rank_character[str(self.rank)])

def match_num_to_card(num):
    '''
    Convert a number(1-52) into a Card object.
    The order of suits is defined in constants.card_suit
    :param num: card number
    :return: a Card object
    '''
    suit = (num - 1) // 13
    rank = num % 13
    if rank == 0:
        rank = 13
    c = Card(card_suit[suit], rank)
    return c

def match_card_to_num(card):
    '''
    Covert a Card object into number.
    :param card: Card object
    :return: number
    '''
    num = card_rank[card.suit] * 13 + card.rank
    return num

def create_half_deck():
    return [Card(j, i) for j in ['diamonds', 'clubs', 'hearts', 'spades'] for i in [1,8,9,10,11,12,13]]

# -------------------sort functions---------------------
# Sort each player object based on their card type. These functions are passed as "key" in the sort function.

def cmp_one_card(player_obj):
    return player_obj.revealed_cards[0]

def cmp_two_cards(player_obj, cards = None):
    if cards is None:
        two_cards = [player_obj.revealed_cards[0], player_obj.revealed_cards[1]]
    else:
        two_cards = cards.copy()
    two_cards.sort()
    if two_cards[0].same_rank(two_cards[1]):  # a pair
        # return a tuple (class type, card number, card suit)
        return ONEPAIR, card_rank_weight[two_cards[0].rank] , card_suit_order[two_cards[1].suit]
    else:  # two cards' numbers are different
        return NOPAIR, card_rank_weight[two_cards[1].rank], card_suit_order[two_cards[1].suit]


def cmp_three_cards(player_obj, cards = None):
    if cards is None:
        three_cards = [player_obj.revealed_cards[0], player_obj.revealed_cards[1], player_obj.revealed_cards[2]]
    else:
        three_cards = cards.copy()
    three_cards.sort()
    if three_cards[0].same_rank(three_cards[1]) and three_cards[0].same_rank(three_cards[2]):
        return TRIPLE, card_rank_weight[three_cards[0].rank], card_suit_order[three_cards[2].suit]
    elif three_cards[0].same_rank(three_cards[1]):
        return ONEPAIR, card_rank_weight[three_cards[0].rank], card_suit_order[three_cards[1].suit]
    elif three_cards[1].same_rank(three_cards[2]):
        return ONEPAIR, card_rank_weight[three_cards[1].rank], card_suit_order[three_cards[2].suit]
    else:
        return NOPAIR, card_rank_weight[three_cards[2].rank], card_suit_order[three_cards[2].suit]


def cmp_four_cards(player_obj, cards = None):
    if cards is None:
        four_cards = [i for i in player_obj.revealed_cards]
    else:
        four_cards = cards.copy()
    four_cards.sort()
    if four_cards[0].same_rank(four_cards[1]) and four_cards[0].same_rank(four_cards[2]) and four_cards[0].same_rank(four_cards[3]):
        return QUADRUPLE, card_rank_weight[four_cards[0].rank], card_suit_order[four_cards[3].suit]
    elif four_cards[0].same_rank(four_cards[1]) and four_cards[0].same_rank(four_cards[2]):
        return TRIPLE, card_rank_weight[four_cards[0].rank], card_suit_order[four_cards[2].suit]
    elif four_cards[1].same_rank(four_cards[2]) and four_cards[1].same_rank(four_cards[3]):
        return TRIPLE, card_rank_weight[four_cards[1].rank], card_suit_order[four_cards[3].suit]
    elif four_cards[0].same_rank(four_cards[1]) and four_cards[2].same_rank(four_cards[3]):
        return TWOPAIR, card_rank_weight[four_cards[2].rank], card_suit_order[four_cards[3].suit]
    elif four_cards[0].same_rank(four_cards[1]):
        return ONEPAIR, card_rank_weight[four_cards[0].rank], card_suit_order[four_cards[1].suit]
    elif four_cards[1].same_rank(four_cards[2]):
        return ONEPAIR, card_rank_weight[four_cards[1].rank], card_suit_order[four_cards[2].suit]
    elif four_cards[2].same_rank(four_cards[3]):
        return ONEPAIR, card_rank_weight[four_cards[2].rank], card_suit_order[four_cards[3].suit]
    elif four_cards[0].same_suit(four_cards[1]) and four_cards[0].same_suit(four_cards[2]) and four_cards[0].same_suit(four_cards[3]):
        if len([card_rank_weight[four_cards[i].rank] for i in range(1, len(four_cards)) if card_rank_weight[four_cards[i].rank] == card_rank_weight[four_cards[i-1].rank]+1]) == 4:
            return STRAIGHTFLUSH, card_rank_weight[four_cards[3].rank], card_suit_order[four_cards[0].suit]
        else:
            return FLUSH, card_rank_weight[four_cards[3].rank], card_suit_order[four_cards[0].suit]
    elif len([card_rank_weight[four_cards[i].rank] for i in range(1, len(four_cards)) if card_rank_weight[four_cards[i].rank] == card_rank_weight[four_cards[i-1].rank]+1]) == 4:
        return STRAIGHT, card_rank_weight[four_cards[3].rank], card_suit_order[four_cards[3].suit]
    else:
        return NOPAIR, card_rank_weight[four_cards[3].rank], card_suit_order[four_cards[3].suit]


def cmp_five_cards(player_obj, cards = None):
    if cards is None:
        five_cards = [i for i in player_obj.cards]
    else:
        five_cards = cards.copy()
    five_cards.sort()
    find_straight = [card_rank_weight[five_cards[i].rank] for i in range(1, len(five_cards)) if card_rank_weight[five_cards[i].rank] == card_rank_weight[five_cards[i-1].rank]+1]
    find_flush = [card_suit_order[five_cards[i].suit] for i in range(1, len(five_cards)) if card_suit_order[five_cards[i].suit] == card_suit_order[five_cards[i-1].suit]]
    find_pair = [five_cards[0]]
    find_triple = [five_cards[0]]
    find_quadruple = [five_cards[0]]
    for c in range(1, len(five_cards)):
        if five_cards[c].rank == five_cards[c-1].rank:
            find_pair.append(five_cards[c])
            find_triple.append(five_cards[c])
            find_quadruple.append(five_cards[c])
        else:
            if len(find_pair) == 2:
                find_pair.append(five_cards[c])
            elif len(find_pair) != 4:
                find_pair.pop()
                find_pair.append(five_cards[c])
            if len(find_triple) != 3:
                find_triple = [five_cards[c]]
            if len(find_quadruple) != 4:
                find_quadruple = [five_cards[c]]

    if len(find_straight) == 4 and len(find_flush) == 4:
        return STRAIGHTFLUSH, card_rank_weight[five_cards[4].rank], card_suit_order[five_cards[4].suit]
    elif len(find_straight) == 4:
        return STRAIGHT, card_rank_weight[five_cards[4].rank], card_suit_order[five_cards[4].suit]
    elif len(find_flush) == 4:
        return FLUSH, card_rank_weight[five_cards[4].rank], card_suit_order[five_cards[4].suit]

    elif len(find_quadruple) == 4:
        return QUADRUPLE, card_rank_weight[find_quadruple[3].rank], card_suit_order[find_quadruple[3].suit]
    elif len(find_triple) == 3 and len(find_pair) >= 4:
        return FULLHOUSE, card_rank_weight[find_triple[2].rank], card_suit_order[find_triple[2].suit]
    elif len(find_triple) == 3:
        return TRIPLE, card_rank_weight[find_triple[2].rank], card_suit_order[find_triple[2].suit]
    elif len(find_pair) == 4:
        return TWOPAIR, card_rank_weight[find_pair[3].rank], card_suit_order[find_pair[3].suit]
    elif len(find_pair) == 2 or len(find_pair) == 3:
        return ONEPAIR, card_rank_weight[find_pair[1].rank], card_suit_order[find_pair[1].suit]
    else:
        return NOPAIR, card_rank_weight[five_cards[4].rank], card_suit_order[five_cards[4].suit]

cmp_func_map = {
    1: cmp_one_card,
    2: cmp_two_cards,
    3: cmp_three_cards,
    4: cmp_four_cards,
    5: cmp_five_cards
}
