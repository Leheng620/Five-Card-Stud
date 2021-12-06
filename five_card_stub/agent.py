from constants import Actions
import random

class AbstractPlayer:
    def __init__(self, balance, index, chip, alive):
        
        self.balance = balance # the player's balance.
        self.index = index
        self.cards = None # all cards on deck
        self.__secret_card = None # the face-down card, only self can access
        self.revealed_cards = None # the cards being revealed to other players
        self.chip = chip # current chip the player has raised
        self.alive = alive
    
    def deepCopy(self):
        '''
        Deepcopy the player object
        '''
        state = AbstractPlayer(self.balance, self.index, self.chip, self.alive)
        state.cards = [card.copy() for card in self.cards]
        state.revealed_cards = state.cards[1:]
        state.__secret_card = state.cards[0]
        return state

class RandomAgent(AbstractPlayer):

    def __init__(self, balance, index, chip, alive, is_uniform=False):
        super(RandomAgent, self).__init__(balance, index, chip, alive)
        self.is_uniform = is_uniform
    
    def deepCopy(self):
        '''
        Deepcopy the player object
        '''
        state = RandomAgent(self.balance, self.index, self.chip, self.alive)
        state.cards = [card.copy() for card in self.cards]
        state.revealed_cards = state.cards[1:]
        state.__secret_card = state.cards[0]
        return state

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
        if self.is_uniform:
            allow_actions = game.get_allow_actions()
            action = random.choice(allow_actions)
        else:
            if game.repeat:
                allow_actions = [Actions.FOLD, Actions.CALL]
                action = random.choices(allow_actions, [1, 2])[0]

            else:
                if self.chip == game.current_max_chips:
                    allow_actions = [Actions.CHECK, Actions.FOLD, Actions.RAISE, Actions.ALL_IN]
                    action = random.choices(allow_actions, [10, 0, 3, 1])[0]
                elif game.current_max_chips == game.max_chips: # there are players have all-in
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
        # print("[debug] player %d, action: %s, raise_chip: %d" % (self.index, action_tup[0], action_tup[1]))
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
        # print("[ACT] player:", self.index, "action:", action, "chip:", self.chip, "balance:", self.balance)

    def append_card(self, card):
        self.cards.append(card)
        self.revealed_cards = self.cards[1:]
    
    def player_checkout(self):
        self.chip = 0        
        self.cards.clear()

    def set_init_cards(self, card_pair):
        self.cards = card_pair
        self.__secret_card = self.cards[0] # the face-down card, only self can access
        self.revealed_cards = self.cards[1:] # the cards being revealed to other players

    

