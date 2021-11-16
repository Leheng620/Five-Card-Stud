from agent import RandomAgent
from constants import Actions, NodeMeta
from copy import deepcopy
from node import Node
import time
import numpy as np
import random

class MCTSAgent(RandomAgent):
    def __init__(self, balance, index, cards, chip, alive):
        '''
        Args:
            root_state:  the game state before each betting round
        '''
        super().__init__(balance, index, cards, chip, alive)
        self.root_state = None
        self.root_node = None
        self.node_count = 0   # The number of node in the tree
        self.n_iterations = 100

    def decide_action(self, game):
        self.root_state = deepcopy(game)                                         # Deepcopy the current game state
        self.root_node = Node(self.node_count, self.index, self.root_state)      # Root Node: current game state
        self.node_count = 0
        for _ in range(self.n_iterations):
            # Keep selecting best child node until the leaf node
            leaf = self.selection()

            # Expand the game tree, appending all the child node to the leaf node
            child = self.expansion(leaf)

            # Simulate at an arbitrary child of node
            winner_id = self.simulation(child)

            # Back-propogate from child to root
            self.back_propagate(winner_id, child)

            print("----------------------------------------")
            print()

        for child in self.root_node.children.values():
            print(child.node_id, child.action, child.N, child.U)
        values = [child.value for child in self.root_node.children.values()]
        child = random.choice([child for child in self.root_node.children.values() if child.value == max(values)])
        action = child.action
        raise_chip = 10 if action == Actions.RAISE else 0

        # game.print_cards()
        return action, raise_chip

    def selection(self):
        '''
        Return a leaf node
        '''
        node = self.root_node
        while len(node.children) > 0:
            values = [child.value for child in node.children.values()]
            node = random.choice([child for child in node.children.values() if child.value == max(values)])
            print("[SELECTION] node: %d" % node.node_id)
        return node

    def expansion(self, node):
        '''
        Append all the child of node
        If node is a terminal node, return node itself; otherwise, return a random child of node
        '''
        print("[EXPANSION] node: %d" % node.node_id)
        state = node.state
        if state.is_round_end():
            state.end_betting_round()
            if state.is_game_end():
                # Game ends, child is a leaf node
                winner = state.get_winner()
                node.outcome = winner
                return node
            else:
                # Game continues, deal cards and start next betting round
                state = state.copyGameState() # Should copy the game state, make sure parent is not ruined
                state.deal()
                state.start_betting_round()

        allow_actions = state.get_allow_actions()

        for action in allow_actions:
            # Update state: next_player act
            new_state = state.copyGameState()       # next_player will act on a copy of the current state
            action_tup = (action, 10 if action == Actions.RAISE else 0)
            curr_player = new_state.get_current_player()
            curr_player.act(new_state, action_tup)
            next_player = new_state.pop_get_next_player()
            self.node_count += 1
            child = Node(self.node_count, next_player.index, new_state, action, node)
            node.add_child(action, child)
        
        return random.choice(list(node.children.values()))

    def simulation(self, node) -> int:
        '''
        Simulate from node till the game ends
        Return the result (winner id)
        '''
        state = node.state.copyGameState()
        while True:
            print("[SIMULATION] round: %d, curr_player: %d" % (state.round, state.curr_player))
            if state.is_round_end():
                state.end_betting_round()
                if state.is_game_end():
                    # Game ends, child is a leaf node
                    winner = state.get_winner()
                    node.outcome = winner
                    return winner
                else:
                    # Game continues, deal cards and start next betting round
                    state.deal()
                    state.start_betting_round()

            action = random.choice(state.get_allow_actions()) # Choose a random action
            action_tup = (action, 10 if action == Actions.RAISE else 0)
            curr_player = state.get_current_player()
            curr_player.act(state, action_tup)
            state.pop_get_next_player()
    
    def back_propagate(self, winner_id, leaf):
        node = leaf
        while node is not None:
            print("[BACK-PROPOGATE] node: %d" % node.node_id)
            node.N += 1
            if node.parent is not None and node.parent.player_id == winner_id:
                node.U += 1
            node = node.parent
        

    # def build_tree(self, state, node):
    #     allow_actions = state.get_allow_actions()
        
    #     print("-------------------------------------------------------")
    #     print("[Expand] node:", node.node_id, ", player:", node.player_id, ", allow_actions:", allow_actions)
    #     for action in allow_actions:
    #         # Update state: next_player act
    #         new_state = state.copyGameState()       # next_player will act on a copy of the current state
    #         action_tup = (action, 10 if action == Actions.RAISE else 0)
    #         curr_player = new_state.get_current_player()
    #         curr_player.act(new_state, action_tup)
    #         next_player = new_state.pop_get_next_player()
    #         self.node_count += 1
    #         child = Node(self.node_count, next_player.index, new_state, action, node)
    #         node.add_child(action, child)
    #         print("[New Child] parent:", node.node_id, ", action:", action, ", child:", child.node_id)


    #         if new_state.is_round_end():
    #             if new_state.is_game_end():
    #                 # Game ends, child is a leaf node
    #                 winner = new_state.get_winner()
    #                 child.outcome = winner
    #                 print("***[Game End] node: %d, winner: player %d" % (child.node_id, winner))
    #             else:
    #                 # Game continues, directly enter next betting round and build tree
    #                 child.mark_deal_needed()  # Mark deal is needed at this node in simulation
    #                 print("***[Round End] node: %d" % (child.node_id))
    #         else:
    #             self.build_tree(new_state, child)
            
    #         print()


        

        
