from agent import RandomAgent
from constants import Actions, NodeMeta
from copy import deepcopy
from node import Node
import time

class MCTSAgent(RandomAgent):
    def __init__(self, balance, index, cards, chip, alive):
        '''
        Args:
            root_state:  the game state before each betting round


        '''
        super().__init__(balance, index, cards, chip, alive)
        self.root_state = None
        self.node_count = 0   # The number of node in the tree

    def decide_action(self, game):
        self.root_state = deepcopy(game)                   # Deepcopy the current game state
        root_node = Node(self.node_count, self.index)      # Root Node: current game state

        self.build_tree(self.root_state, root_node)

        # simulation and update the tree
        self.simulation() 

        # Select an action at the root node
        action = self.selection() 

        raise_chip = 10 if action == Actions.RAISE else 0
        return action, raise_chip

    def build_tree(self, state, node):
        allow_actions = state.get_allow_actions(state.get_current_player())
        
        print("-------------------------------------------------------")
        print("[Expand] node:", node.node_id, ", player:", node.player_id, ", allow_actions:", allow_actions)
        for action in allow_actions:
            # Update state: next_player act
            new_state = state.copyGameState()       # next_player will act on a copy of the current state
            action_tup = (action, 10 if action == Actions.RAISE else 0)
            curr_player = new_state.get_current_player()
            curr_player.act(new_state, action_tup)
            next_player = new_state.pop_get_next_player()
            self.node_count += 1
            child = Node(self.node_count, next_player.index, action, node, new_state)
            node.add_child(action, child)
            print("[New Child] parent:", node.node_id, ", action:", action, ", child:", child.node_id)

            # time.sleep(1)

            if new_state.is_round_end():
                if new_state.is_game_end():
                    # Game ends, child is a leaf node
                    winner = new_state.get_winner()
                    child.outcome = winner
                    print("***[Game End] node: %d, winner: player %d" % (child.node_id, winner))
                else:
                    # Game continues, directly enter next betting round and build tree
                    child.mark_deal_needed()  # Mark deal is needed at this node in simulation
                    print("***[Round End] node: %d" % (child.node_id))
            else:
                self.build_tree(new_state, child)
            
            print()

        
    def simulation(self):
        pass
    
    def selection(self):
        return Actions.CHECK


        

        
