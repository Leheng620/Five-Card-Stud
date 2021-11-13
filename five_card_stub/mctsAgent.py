from agent import Agent
from gameState import GameState
from copy import deepcopy
from node import Node

class MCTSAgent(Agent):
    def __init__(self, root_state):
        '''
        Args:
            root_state: 
        '''
        self.root_state = deepcopy(root_state)
        self.root_node = Node()
        self.node_count = 1

    

