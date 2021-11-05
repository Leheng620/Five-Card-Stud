from unittest import TestCase
import random

from card import Card
from constants import *



def create_card(suit, rank):
    '''
        0: 'blade'
        1: 'heart'
        2: 'brick'
        3: 'club'
    '''
    return Card(card_suit[suit], rank)


class CardTest(TestCase):

    def test_card_equal(self):
        full_deck1 = [Card(j, i) for j in ['brick', 'club', 'heart', 'blade'] for i in range(1, 14)]
        full_deck2 = [Card(j, i) for j in ['brick', 'club', 'heart', 'blade'] for i in range(1, 14)]
        for c1, c2 in zip(full_deck1, full_deck2):
            TestCase.assertTrue(self, c1 == c2)


    def test_card_comparison(self):

        sorted_card_list = []
        for rank in list(range(2, 14)) + [1]:
            for suit in list(card_suit_order.keys())[::-1]:
                sorted_card_list.append(Card(suit, rank))

        full_deck = [Card(j, i) for j in ['brick', 'club', 'heart', 'blade'] for i in range(1, 14)]
        random.shuffle(full_deck)

        full_deck.sort()

        for yi, y in zip(full_deck, sorted_card_list):
            TestCase.assertTrue(self, yi == y)



class CardTypeComparisonTest(TestCase):
    def test_cmp_two_cards(self):
        card1 = (create_card(0, 1), create_card(2, 2))
        card2 = (create_card(1, 1), create_card(3, 2))
        TestCase.assertTrue(self, card1 > card2)