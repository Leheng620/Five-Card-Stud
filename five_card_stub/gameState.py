from agent import Agent
from card import *
from random import shuffle
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
        total_chips:    the total number of chips on the table
        card_stack:     cards in the heap, shuffled
        first_player:   Index of the player with best cards (among the alive players), 
                        betting & dealling start from this player
        '''
        self.round = 1
        self.n_players = n_players
        self.players = None
        self.alive_indices = list(range(n_players))
        self.player_queue = deque()
        self.total_chips = 0
        self.card_stack = deque(create_half_deck())
        shuffle(self.card_stack)
        self.print_card_stack()

        self.initializePlayers(balance, ante)
        self.first_player = 0

    def initializePlayers(self, balance, ante):
        '''
        Deal two cards to each player, and initialize the players array
        '''
        init_card_pairs = [[] for _ in range(self.n_players)]
        for _ in range(2):
            for i in self.alive_indices:
                top_card = self.card_stack.popleft()
                init_card_pairs[i].append(top_card)
        self.players = [Agent(balance-ante, i, card_pair, ante, True) for i, card_pair in enumerate(init_card_pairs)]

    def deal(self):
        '''
        Deal one card to each alive player, increment the round count
        '''
        ordering = self.alive_indices[self.first_player:] + self.alive_indices[:self.first_player]
        for i in ordering:
            player = self.players[i]
            top_card = self.card_stack.popleft()
            player.append_card(top_card)
        
        self.round += 1

    def get_next_player(self):
        player_idx = self.player_queue.popleft()
        self.player_queue.append(player_idx)

        return self.players[player_idx]
    
    def build_player_queue(self):
        '''
        Compare revealed cards and return the player with best card
        '''
        alive_p = self.get_alive_players()
        alive_p.sort(key=cmp_func_map[self.round])
        self.first_player = alive_p[-1].index
        self.player_queue.extend(self.alive_indices[self.first_player:] + self.alive_indices[:self.first_player])
    
    def get_player_queue(self):
        return self.player_queue
    
    def clear_player_queue(self):
        self.player_queue.clear()

    def get_alive_players(self):
        return [self.players[i] for i in self.alive_indices]

    def is_round_end(self):
        if len(self.get_alive_players()) < 2:
            return True
        for p in self.get_alive_players():
            if p.last_action != Actions.CHECK:
                return False
        return True

    def is_game_end(self):
        return self.round == 4 or len(self.alive_indices) < 2

    def player_act(self, player_id, action, raise_chip=0):
        if action == Actions.FOLD:
            self.alive_indices.remove(player_id)
        elif action == Actions.RAISE:
            self.total_chips += raise_chip

# Functions for debugging
    def print_cards(self):
        '''
        Helper function for debugging
        '''
        for p in self.players:
            print("Player %d" % p.index)
            for c in p.cards:
                print(str(c), sep=', ', end='; ')
            print()
        print("------------------------------")

    def print_card_stack(self):
        for c in self.card_stack:
            print(c.suit, c.rank, sep=', ', end='; ')
        print()






