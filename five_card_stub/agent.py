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

class RandomAgent(AbstractPlayer):

    def __init__(self, balance, index, cards, chip, alive):
        super(RandomAgent, self).__init__(balance, index, cards, chip, alive)

    def decide_action(self, game):
        '''
        Should be overwritten by sub class
        :param game: gameState object
        :param repeat: see game.py
        :return: Action, raise_chip
        '''
        # all alive players have all-in
        if self.chip == game.max_chips:
            return Actions.CHECK, 0

        raise_chip = 0
        if game.repeat:
            allow_actions = [Actions.FOLD, Actions.CALL]
            action = random.choices(allow_actions, [1, 2])[0]

        else:
            if self.chip == game.current_max_chips:
                allow_actions = [Actions.CHECK, Actions.FOLD, Actions.RAISE, Actions.ALL_IN]
                action = random.choices(allow_actions, [10, 0, 3, 1])[0]
            elif game.current_max_chips == game.current_max_chips: # there are players have all-in
                allow_actions = [Actions.FOLD, Actions.CALL]
                action = random.choices(allow_actions, [2, 3])[0]
            else: # there are players have raised
                allow_actions = [Actions.FOLD, Actions.CALL, Actions.RAISE, Actions.ALL_IN]
                action = random.choices(allow_actions, [1, 8, 3, 1])[0]

            if action == Actions.RAISE:
                raise_chip = 10 # fix the raised amount

        return action, raise_chip

    def play(self, game):
        '''
        Decide an action and act it
        '''
        action_tup = self.decide_action(game)
        self.act(game, action_tup)

    def act(self, game, action_tup):
        action, raise_chip = action_tup
        # the difference between the amount of chip a player has and the current max chip on table
        chip_diff = game.current_max_chips - self.chip
        if action == Actions.FOLD:
            self.alive = False
        elif action == Actions.RAISE:
            # RAISE + CALL/CHECK
            # raised amount + the amount other players have raised in the current round
            chip_diff = raise_chip + chip_diff
            self.balance -= chip_diff
            self.chip += chip_diff
        elif action == Actions.ALL_IN:
            raise_chip = game.max_chips - game.current_max_chips
            chip_diff = raise_chip + chip_diff
            self.balance -= chip_diff
            self.chip += chip_diff
        elif action == Actions.CALL:
            self.balance -= chip_diff
            self.chip += chip_diff

        game.player_act(self.index, action, raise_chip, chip_diff)
        print("[player.act] player %d, action: %s, raise_chip: %d, chip_diff: %d, self.chip: %d" % (self.index, action.name, raise_chip, chip_diff, self.chip))

    def append_card(self, card):
        self.cards.append(card)
        self.revealed_cards = self.cards[1:]
    
    def get_allow_actions(self, game):
        if game.repeat:
            return [Actions.FOLD, Actions.CALL]
        else:
            if self.chip == game.current_max_chips:
                return [Actions.CHECK, Actions.FOLD, Actions.RAISE, Actions.ALL_IN]
            elif game.current_max_chips == game.current_max_chips: # there are players have all-in
                return [Actions.FOLD, Actions.CALL]
            else: # there are players have raised
                return [Actions.FOLD, Actions.CALL, Actions.RAISE, Actions.ALL_IN]


