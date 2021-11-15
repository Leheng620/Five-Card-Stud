from agent import RandomAgent
from constants import Actions, NodeMeta
from copy import deepcopy
from node import Node

class MCTSAgent(RandomAgent):
    def __init__(self, balance, index, cards, chip, alive):
        '''
        Args:
            root_state:  the game state before each betting round


        '''
        super().__init__(balance, index, cards, chip, alive)
        self.root_state = None
        self.node_count = 0   # The number of node in the tree

    # def decide_action(self, game):
    #     self.root_state = deepcopy(game)     # Deepcopy the current game state
    #     root_node = Node(self.node_count, self.index)      # Root Node: current game state

    #     self.build_tree(self.root_state, root_node)

    #     action = argmax(root_node.children.value)

    #     raise_chip = 10 if action == Actions.RAISE else 0
    #     return action, raise_chip

    # def build_tree(self, state, node):
        


    #     possible_actions = list(Actions)
    #     if self.repeat:
    #         possible_actions = [Actions.CALL, Actions.FOLD]

    #     for action in possible_actions:
    #         new_state = deepcopy(state)   # next_player will act on a copy of the current state
    #         next_player = new_state.get_next_player()  # Player in the child node
    #         self.node_count += 1
    #         child = Node(self.node_count, next_player.index, action, node)
    #         node.add_child(action, child)
    #         next_player.play(new_state, self.repeat)
    #         self.build_tree(new_state, child)
        



        

        
