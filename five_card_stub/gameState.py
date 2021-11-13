from agent import RandomAgent
from card import *
import random
from collections import deque

class GameState:
    def __init__(self, n_players=2, balance=100, ante=5):
        '''
        round:          rounds of card dealing so far
                        round 0 => two cards each player
                        rount 1-3 => one card each player
        players:        all the players
        alive_indices:  indecies of players still alive, initially [0, n_players-1]
        player_queue:   queue of players indices (in the order of play in the current betting round)
        total_chips:    the total number of chips on the table (including chips put in by both alive or not alive players)
        max_chips:      the maximum number of chips put in among all the players,
        current_max_chips: The max chips on the table in the current round. If any player has chips that is less than
                        current_max_chips, the player can call, raise, or fold, but can't check. Alive players have to
                        put in the same number (in total) to stay alive
        used_cards:     The cards that have been dealt to players.
        first_player:   Index of the player with best cards (among the alive players), 
                        betting & dealling start from this player
        ante:           The price of the entrance ticket
        '''
        self.round = 1
        self.n_players = n_players
        self.players = None
        self.alive_indices = list(range(n_players))
        self.player_queue = deque()
        self.total_chips = 0
        self.max_chips = 0
        self.current_max_chips = 0
        self.used_card = set()
        self.initializePlayers(balance, ante)
        self.first_player = 0
        self.ante = ante
        self.initialize_game_state()

    def initializePlayers(self, balance, ante) -> None:
        '''
        Deal two cards to each player, and initialize the players array.
        balance: initial balance each player has
        ante: the price of the entrance ticket
        '''
        init_card_pairs = [[] for _ in range(self.n_players)]
        for _ in range(2):
            for i in self.alive_indices:
                top_card = self.generate_random_card()
                init_card_pairs[i].append(top_card)
        self.players = [RandomAgent(balance-ante, i, card_pair, ante, True) for i, card_pair in enumerate(init_card_pairs)]

    def initialize_game_state(self):
        # The maximum chips players can bet (when all in) is the lowest balance a player has among all players.
        self.max_chips = min([p.balance for p in self.players])

        # The max chip in the current round is the price of the entrance ticket,
        # which also equals to the chip each player has on table at the beginning
        self.current_max_chips = self.ante

        # the total chips of the game state at the beginning is the sum of entrance ticket
        self.total_chips = self.ante * len(self.players)

    def deal(self) -> None:
        '''
        Deal one card to each alive player, increment the round count
        '''
        ordering = self.alive_indices[self.first_player:] + self.alive_indices[:self.first_player]
        for i in ordering:
            player = self.players[i]
            top_card = self.generate_random_card()
            player.append_card(top_card)
        
        self.round += 1

    def generate_random_card(self):
        '''
        Generate a random card from the remaining card deck. Then eliminate it from the remaining card deck.
        :return: The random card generated.
        '''

        cards = create_half_deck()
        generated_card = random.choice([card for card in cards if card not in self.used_card])
        self.used_card.add(generated_card)
        return generated_card


    def get_next_player(self) -> RandomAgent:
        player_idx = self.player_queue.popleft()
        self.player_queue.append(player_idx)

        return self.players[player_idx]
    
    def build_player_queue(self) -> None:
        '''
        Compare revealed cards and return the player with best card
        '''
        alive_p = self.get_alive_players()
        alive_p.sort(key=cmp_func_map[self.round])
        self.first_player = alive_p[-1].index
        self.player_queue.extend(self.alive_indices[self.first_player:] + self.alive_indices[:self.first_player])
    
    def clear_player_queue(self):
        self.player_queue.clear()

    # Interface provided to the agent
    def player_act(self, player_id, action, raise_chip=0):
        if action == Actions.FOLD:
            self.alive_indices.remove(player_id)
            return
        elif action == Actions.RAISE or action == Actions.ALL_IN:
            self.current_max_chips += raise_chip
            self.total_chips += raise_chip
        elif action == Actions.CALL:
            self.total_chips += raise_chip
        
        # self.total_chips +=
         


    # Conditions for a round/game to end
    def is_round_end(self):
        '''
        The current round is not end only when there is player that does not have the same of amount of chips on table
        as the current_max_chips, they still need to decide whether to fold or call.
        '''
        if len(self.get_alive_players()) < 2:
            return True
        for p in self.get_alive_players():
            if p.chip != self.current_max_chips:
                return False
        return True

    def is_game_end(self):
        return self.round == 4 or len(self.alive_indices) < 2

    def get_winner(self):
        alive_p = self.get_alive_players()
        if len(alive_p) == 1:
            return alive_p[0].index
        alive_p.sort(key=cmp_func_map[5])
        return alive_p[-1].index


    # Get methods
    def get_player_queue(self):
        return self.player_queue

    def get_alive_players(self):
        return [self.players[i] for i in self.alive_indices]

    # Functions for debugging
    def print_cards(self):
        '''
        Helper function for debugging
        '''
        print("------------------------------")
        for p in self.players:
            print("Player %d" % p.index)
            for c in p.cards:
                print(str(c), sep=', ', end='; ')
            print()







