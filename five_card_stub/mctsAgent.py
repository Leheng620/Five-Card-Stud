from agent import RandomAgent
from constants import Actions, NodeMeta
from gameState import GameState
from copy import deepcopy
from node import Node

class MCTSAgent(RandomAgent):
    def __init__(self, root_state, balance, index, cards, chip, alive, n_players=2):
        '''
        Args:
            root_state:  the game state before this betting round
            root_node:   node that represents the root state
            raise_limit: the maximum time of raises in each betting round
            all_in:      True if one of the players choose ALL_IN; False otherwise
            node_count:  the number of nodes in MCTS (for statistics)
        '''
        super().__init__(balance, index, cards, chip, alive)
        self.root_state = deepcopy(root_state)
        self.root_node = Node(index=0, raise_limit=NodeMeta.RAISE_LIMIT)
        self.node_count = 0
        self.n_players = n_players




