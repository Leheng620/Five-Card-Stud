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
        self.n_iterations = NodeMeta.N_ITERATIONS

    def decide_action(self, game):
        self.root_state = deepcopy(game)                                         # Deepcopy the current game state
        self.root_node = Node(self.node_count, self.index, self.root_state)      # Root Node: current game state
        self.node_count = 0
        for _ in range(self.n_iterations):
            # Keep selecting best child node until the leaf node
            leaf = self.selection()

            time.sleep(3)

            # Expand the game tree, appending all the child node to the leaf node
            child = self.expansion(leaf)

            time.sleep(3)

            # Simulate at an arbitrary child of node
            winner_id = self.simulation(child)

            time.sleep(3)

            # Back-propogate from child to root
            self.back_propagate(winner_id, child)

            time.sleep(3)

            print("----------------------------------------")
            print()

        for child in self.root_node.children:
            print(child.node_id, child.action, child.N, child.U)
        action = max(self.root_node.children, key=self.root_node.children.get)
        raise_chip = 10 if action == Actions.RAISE else 0
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
                print("***[Game End] node: %d, winner: player %d" % (node.node_id, winner))
                return node
            else:
                # Game continues, deal cards and start next betting round
                state = state.copyGameState() # Should copy the game state, make sure parent is not ruined
                state.deal()
                state.print_cards()
                state.start_betting_round()
                print("***[Round End] node: %d" % (node.node_id))

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
            print("[New Child] parent:", node.node_id, ", action:", action, ", child:", child.node_id)
            print()
        
        return random.choice(list(node.children.values()))

    def simulation(self, node) -> int:
        '''
        Simulate from node till the game ends
        Return the result (winner id)
        '''
        state = node.state.copyGameState()
        while True:
            if state.is_round_end():
                state.end_betting_round()
                if state.is_game_end():
                    # Game ends, child is a leaf node
                    winner = state.get_winner()
                    node.outcome = winner
                    print("***[Game End] node: %d, winner: player %d" % (node.node_id, winner))
                    return winner
                else:
                    # Game continues, deal cards and start next betting round
                    state.deal()
                    state.print_cards()
                    state.start_betting_round()
                    print("***[Round End] node: %d" % (node.node_id))

            action = random.choice(state.get_allow_actions()) # Choose a random action
            action_tup = (action, 10 if action == Actions.RAISE else 0)
            curr_player = state.get_current_player()
            curr_player.act(state, action_tup)
            next_player = state.pop_get_next_player()
            print("[SIMULATION] %d -> %d" % (curr_player.index, next_player.index))
    
    def back_propagate(self, winner_id, leaf):
        node = leaf
        while node is not None:
            print("[BACK-PROPOGATE] node: %d" % node.node_id)
            node.N += 1
            if node.player_id == winner_id:
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

    #         # time.sleep(1)

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


        

        
