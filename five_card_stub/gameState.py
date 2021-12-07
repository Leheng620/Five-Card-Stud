from agent import RandomAgent
from card import *
import random
from collections import deque
from mctsAgent import MCTSAgent

class GameState:
    def __init__(self, n_players=2, balance=100, ante=5, prevState=None):
        '''
        round:          rounds of card dealing so far
                        round 0 => two cards each player
                        rount 1-3 => one card each player
        players:        all the players
        alive_indices:  indecies of players still alive, initially [0, n_players-1]
        player_queue:   queue of players indices (in the order of play in the current betting round)
        total_chips:    the total number of chips on the table (including chips put in by both alive or not alive players)
        max_chips:      the maximum number of chips can be put in by a player (the all-in amount)
        current_max_chips: The max chips on the table in the current round. If any player has chips that is less than
                        current_max_chips, the player can't check. Alive players have to
                        put in the same number (in total) to stay alive
        used_cards:     The cards that have been dealt to players.
        first_player:   Index of the player with best cards (among the alive players), 
                        betting & dealling start from this player
        ante:           The price of the entrance ticket
        repeat:         Bool. repeat is set to False at the beginning of each betting round;
                        set to True when all the players has been processed once
        num_alive_players_not_been_processed:     
                        the number of players that have not taken an action yet
        '''
        if prevState != None:
            self.round = prevState.round
            self.n_players = prevState.n_players
            self.players = list(prevState.players)
            self.alive_indices = prevState.alive_indices[:]
            self.total_chips = prevState.total_chips
            self.max_chips = prevState.max_chips
            self.used_card = prevState.used_card.copy()
            self.ante = prevState.ante
            self.current_max_chips = prevState.current_max_chips
            self.balance = prevState.balance

            self.player_queue = prevState.player_queue.copy()
            self.curr_player = prevState.curr_player
            self.repeat = prevState.repeat
            self.num_alive_players_not_been_processed = prevState.num_alive_players_not_been_processed
            self.first_player = prevState.first_player

        else:
            self.round = 1
            self.n_players = n_players
            self.players = None
            self.alive_indices = list(range(n_players))
            self.total_chips = 0
            self.max_chips = 0
            self.used_card = set()
            self.ante = ante
            self.current_max_chips = 0
            self.balance = balance

            # Info for betting round
            self.player_queue = deque()
            self.curr_player = None
            self.repeat = False
            self.num_alive_players_not_been_processed = 0
            self.first_player = None

    def deepCopy(self):
        state = GameState(prevState=self)
        state.players = [player.deepCopy() for player in self.players]
        state.alive_indices = [i for i in self.alive_indices]
        state.used_card = set()
        for c in self.used_card:
            state.used_card.add(c)
        state.player_queue = deque(self.player_queue)
        return state

    def initializePlayers(self, algorithm="mcts_vs_uniform", MCTS_iterations=None) -> None:
        '''
        Deal two cards to each player, and initialize the players array.

        Args:
            algorithm:
                Algorithm to use for each player
            MCTS_iterations:
                integer or List[integer]. 
                When algorithm is "mcts_vs_random" or "mcts_vs_uniform", MCTS_iterations should be an integer
                When algorithm is "mcts_vs_mcts", MCTS_iterations should be a list of integer of length 2
        '''
        if algorithm == "random_vs_uniform":
            self.players = [RandomAgent(self.balance, 0, 0, True), RandomAgent(self.balance, 1, 0, True, is_uniform=True)]
        elif algorithm == "mcts_vs_random":
            self.players = [MCTSAgent(self.balance, 0, 0, True, MCTS_iterations), RandomAgent(self.balance, 1, 0, True)]
        elif algorithm == "mcts_vs_uniform":
            self.players = [MCTSAgent(self.balance, 0, 0, True, MCTS_iterations), RandomAgent(self.balance, 1, 0, True, is_uniform=True)]
        elif algorithm == "mcts_vs_mcts":
            if MCTS_iterations is None:
                self.players = [MCTSAgent(self.balance, i, 0, True) for i in range(self.n_players)]
            else:  
                if type(MCTS_iterations) is not list or len(MCTS_iterations) < 2:
                    raise Exception("mcts_vs_mcts only accepts list of length 2")
                self.players = [MCTSAgent(self.balance, i, 0, True, n_iterations=MCTS_iterations[i]) for i in range(2)]
        else:
            self.players = [RandomAgent(self.balance, i, 0, True) for i in range(self.n_players)]

    def initialize_game_state(self):
        # Reset game state
        self.round = 1
        self.used_card.clear()

        # Mark all players as alive
        self.alive_indices = list(range(self.n_players))
        self.curr_player = None

        # The maximum chips players can put in (when all in) is the lowest balance a player has among all players.
        self.max_chips = min([p.balance for p in self.players])

        # The max chip in the current round is the price of the entrance ticket,
        # which also equals to the chip each player has on table at the beginning
        self.current_max_chips = self.ante

        # the total chips of the game state at the beginning is the sum of entrance ticket
        self.total_chips = self.ante * len(self.players)

        self.pay_entrance_ticket()

        # Deal two cards to each player
        init_card_pairs = [[] for _ in range(self.n_players)]
        for _ in range(2):
            for i in self.alive_indices:
                top_card = self.generate_random_card()
                init_card_pairs[i].append(top_card)
        for i, p in enumerate(self.players):
            p.alive = True
            p.set_init_cards(init_card_pairs[i])



    def checkout(self):
        '''
        Give self.total_chips to the winner
        '''
        winner_p = self.players[self.get_winner()]
        winner_p.balance += self.total_chips
        self.total_chips = 0

        # Checkout each player
        for p in self.players:
            p.player_checkout()

    def pay_entrance_ticket(self):
        for i, p in enumerate(self.players):
            if p.balance < self.ante:
                raise Exception("Player %d does not have enough balance to play." % i)
            p.balance -= self.ante
            p.chip += self.ante

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

    # Interface for starting and ending a betting round

    def start_betting_round(self):
        self.build_player_queue()
        self.repeat = False
        self.num_alive_players_not_been_processed = len(self.alive_indices)
    
    def end_betting_round(self):
        self.clear_player_queue()
        self.clear_raise_flag()

    # Utility functions for player queue
    def get_current_player(self) -> RandomAgent:
        '''
        Return the current player
        '''
        return self.players[self.curr_player]

    def pop_get_next_player(self) -> RandomAgent:
        '''
        Pop next player from qeueu and append it at the end
        (Update the current player)
        Return the next player
        '''
        player_idx = self.player_queue.popleft()
        self.curr_player = player_idx
        self.player_queue.append(player_idx)

        return self.players[player_idx]

    def get_next_player(self) -> RandomAgent:
        '''
        Return the first player in the queue without modifying the queue
        '''
        return self.players[self.player_queue[0]]
    
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
    
    def clear_raise_flag(self):
        for p in self.get_alive_players():
            p.has_raised = False

    # Interface provided to the agent
    def player_act(self, player_id, action, raise_chip, chip_diff):
        if action == Actions.FOLD:
            self.alive_indices.remove(player_id)
            return
        elif action == Actions.RAISE or action == Actions.ALL_IN:
            self.current_max_chips += raise_chip
            self.total_chips += chip_diff
        elif action == Actions.CALL:
            self.total_chips += chip_diff
         
        self.num_alive_players_not_been_processed -= 1

    # Conditions for a round/game to end
    def is_round_end(self):
        '''
        The current round is not end only when there is player that does not have the same of amount of chips on table
        as the current_max_chips, they still need to decide whether to fold or call.

        When repeat is True, every player has made an action, and all players has either raised or checked once, then
        the only action left for them is either fold or call. The idea is that every player can only take up to
        2 actions in a single round
        '''
        if len(self.alive_indices) < 2:
            return True
        elif self.num_alive_players_not_been_processed > 0 and self.repeat:
            if self.all_alive_player_has_decided():
                return True
        elif self.num_alive_players_not_been_processed == 0 and self.repeat:
            return True
        elif self.num_alive_players_not_been_processed == 0 and not self.repeat:
            if self.all_alive_player_has_decided():
                return True
            else:
                self.repeat = True
                self.num_alive_players_not_been_processed = len(self.alive_indices)
        return False
        
    def all_alive_player_has_decided(self):
        '''
        Return true if all the alive player has been asked once; false otherwise
        '''
        for p in self.get_alive_players():
            if p.chip != self.current_max_chips:
                return False
        return True

    def get_allow_actions(self):
        '''
        Return allowed actions of the current player
        '''
        player = self.get_current_player()
        # print("[ALLOW_ACTIONS] player.chip: %d, current_max_chip: %d, max_chip: %d" % (player.chip, self.current_max_chips, self.max_chips))

        if self.repeat:
            # All the player has checked or raised or someone all-in
            return [Actions.FOLD, Actions.CALL]
        elif player.chip == self.max_chips:
            return [Actions.CHECK]
        else:
            if player.chip == self.current_max_chips:
                return [Actions.FOLD, Actions.CHECK, Actions.RAISE]
            else: # there are players have raised
                if player.chip == self.current_max_chips:
                    return [Actions.CHECK, Actions.FOLD, Actions.RAISE]
                elif self.current_max_chips == self.max_chips:  # there are players have all-in
                    return [Actions.FOLD, Actions.CALL]
                else:
                    return [Actions.FOLD, Actions.CALL, Actions.RAISE]
                # if player.balance > self.current_max_chips - player.chip:
                #     return [Actions.FOLD, Actions.CALL, Actions.RAISE]
                # elif player.balance == self.current_max_chips - player.chip:
                #     return [Actions.FOLD, Actions.CALL]
                # else:
                #     return [Actions.FOLD]


    def is_game_end(self):
        return self.round == 4 or len(self.alive_indices) < 2

    def get_winner(self):
        alive_p = self.get_alive_players()
        if len(alive_p) == 1:
            return alive_p[0].index
        alive_p.sort(key=cmp_func_map[5])
        return alive_p[-1].index
    
    def is_terminal(self):
        for p in self.players:
            if p.balance < self.ante:
                return True
        return False

    # Get methods
    def get_player_queue(self):
        return self.player_queue

    def get_alive_players(self):
        return [self.players[i] for i in self.alive_indices]


    # Functions for debugging
    def print_revealed_cards(self):
        '''
        Helper function for debugging
        '''
        debug("------------------------------")
        for p in self.players:
            debug("Player %d" % p.index)
            for c in p.revealed_cards:
                debug(str(c), sep=', ', end='; ')
            debug()

    def print_cards(self):
        '''
        Helper function for debugging
        '''
        debug("------------------------------")
        for p in self.players:
            debug("Player %d" % p.index)
            for c in p.cards:
                debug(str(c), sep=', ', end='; ')
            debug()
    
    def print_all_player_balance(self):
        '''
        Print the balance of each player
        '''
        for p in self.players:
            debug("Player %d balance is %d" % (p.index, p.balance))

    def print_results(self):
        debug("Results:")
        for p in self.players:
            debug("[Player %d] balance: %d" % (p.index, p.balance))
