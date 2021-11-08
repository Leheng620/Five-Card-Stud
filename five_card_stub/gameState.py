from agent import Agent
from card import *
from random import shuffle
from collections import deque

class GameState:
    def __init__(self, n_players, balance):
        '''
        round:            rounds of card dealing so far
                          round 0 => two cards each player
                          rount 1-3 => one card each player
        to_player:        the next player to act
        players:          all the players
        alive_indices:    indecies of players still alive, initially [0, n_players-1]
        chip:             the chips on the table
        card_stack:       cards in the heap
        '''
        self.round = 0
        self.to_play = None
        self.players = [Agent(balance, i, [], 0, True) for i in range(n_players)]
        self.alive_indices = list(range(n_players))
        self.player_queue = deque()
        self.total_chips = 0
        self.card_stack = deque(create_half_deck())
        shuffle(self.card_stack)

    def deal(self):
        '''
        Deal cards to each alive player
        '''
        dealing_rounds = 2 if self.round == 0 else 1

        for _ in range(dealing_rounds):
            for i in self.alive_indices:
                player = self.players[i]
                top_card = self.card_stack.popleft()
                player.append_card(top_card)
                self.card_stack
        
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
        idx = alive_p[0].index
        self.player_queue.extend(self.alive_indices[idx:] + self.alive_indices[:idx])
    
    def get_player_queue(self):
        return self.player_queue
    
    def clear_player_queue(self):
        self.player_queue.clear()

    def get_alive_players(self):
        return [self.players[i] for i in self.alive_indices]

    def is_round_end(self):
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

    def print_cards(self):
        '''
        Helper function for debugging
        '''
        for p in self.players:
            print("Player %d" % p.index)
            for c in p.cards:
                print(c.suit, c.rank, sep=', ')
            print()
        print("------------------------------")






