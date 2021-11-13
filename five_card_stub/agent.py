from constants import Actions
import random

class AbstractPlayer:
    def __init__(self, balance, index, cards, chip, alive):
        self.balance = balance # the player's balance.
        self.index = index
        self.cards = cards # all cards on deck
        self.__secret_card = cards[0] # the face-down card, only self can access
        self.revealed_cards = cards[1:] # the cards being revealed to other players
        self.chip = chip # current chip the player has raised
        self.alive = alive
        self.last_action = None


class RandomAgent(AbstractPlayer):

    def __init__(self, balance, index, cards, chip, alive):
        super(RandomAgent, self).__init__(balance, index, cards, chip, alive)

    def decide_action(self, game, repeat):
        '''
        Should be overwritten by sub class
        :param game: gameState object
        :param repeat: see game.py
        :return: Action, raise_chip
        '''
        raise_chip = 0
        if repeat:
            allow_actions = [Actions.FOLD, Actions.CALL]
            action = random.choices(allow_actions, [1, 2])[0]

        else:
            if self.chip == game.current_max_chips:
                allow_actions = [Actions.CHECK, Actions.FOLD, Actions.RAISE, Actions.ALL_IN]
                action = random.choices(allow_actions, [10, 0, 3, 1])[0]
            else:
                allow_actions = [Actions.FOLD, Actions.CALL, Actions.RAISE, Actions.ALL_IN]
                action = random.choices(allow_actions, [1, 8, 3, 1])[0]
            if action == Actions.RAISE:
                raise_chip = 10

        return action, raise_chip

    def play(self, game, repeat):
        action, raise_chip = self.decide_action(game, repeat)
        if action == Actions.FOLD:
            self.alive = False
        elif action == Actions.RAISE:
            self.balance -= raise_chip
            self.chip += raise_chip
        elif action == Actions.ALL_IN:
            raise_chip = game.max_chips - self.chip
            self.balance -= raise_chip
            self.chip += raise_chip
        elif action == Actions.CALL:
            raise_chip = game.current_max_chips - self.chip
            self.balance -= raise_chip
            self.chip += raise_chip

        game.player_act(self.index, action, raise_chip)
        print("[debug] player %d, action: %s, raise_chip: %d" % (self.index, action.name, raise_chip))
        self.last_action = action
    
    def append_card(self, card):
        self.cards.append(card)
        self.revealed_cards = self.cards[1:]



