from constants import Actions
import random

class AbstractPlayer:
    def __init__(self, balance, index, cards, chip, alive):
        self.balance = balance
        self.index = index
        self.cards = cards
        self.revealed_cards = cards[1:]
        self.chip = chip
        self.alive = alive
        self.last_action = None


class Agent(AbstractPlayer):

    def __init__(self, balance, index, cards, chip, alive):
        super(Agent, self).__init__(balance, index, cards, chip, alive)

    def decide_action(self, game):
        if self.index == 0 and self.last_action == Actions.CHECK:
            return (Actions.RAISE, 1)
        else:
            return (Actions.CHECK, 0)

    def play(self, game):
        action, raise_chip = self.decide_action(game)
        if action == Actions.FOLD:
            self.alive = False
        elif action == Actions.RAISE:
            self.balance -= raise_chip
            self.chip += raise_chip

        game.player_act(self.index, action, raise_chip)
        self.last_action = action
    
    def append_card(self, card):
        self.cards.append(card)
        self.revealed_cards = self.cards[1:]



