from agent import Agent
from constants import Action, NodeMeta, POSSIBLE_ACTIONS
from gameState import GameState
from copy import deepcopy
from node import Node

class MCTSAgent(Agent):
    def __init__(self, root_state, n_players=2):
        '''
        Args:
            root_state:  the game state before this betting round
            root_node:   node that represents the root state
            raise_limit: the maximum time of raises in each betting round
            all_in:      True if one of the players choose ALL_IN; False otherwise
            node_count:  the number of nodes in MCTS (for statistics)
        '''
        self.root_state = deepcopy(root_state)
        self.root_node = Node(index=0, raise_limit=NodeMeta.RAISE_LIMIT)
        self.node_count = 0
        self.n_players = n_players
        self.search_tree = self.buildTree(self.root_node)

    def buildTree(self, node: Node):
        '''
        Recursively append children to the `node`
        '''
        if node.action == Action.FOLD or node.consecutive_checks == self.n_players - 1:
            return
        actions = POSSIBLE_ACTIONS
        print(actions)
        if node.raise_limit == 0:
            actions.remove(Action.RAISE)
            actions.remove(Action.ALL_IN)
        print(actions)
        children = {}
        for a in actions:
            raise_limit = node.raise_limit - 1 if a == Action.RAISE else node.raise_limit
            consecutive_checks = node.consecutive_checks + 1 if a == Action.CHECK and node != self.root_node else 0
            self.node_count += 1
            child = Node(a, node, raise_limit, self.node_count, consecutive_checks)
            self.buildTree(child)
            children[a] = child
        node.add_children(children)

        # For debugging
        print(node.index, end=': ')
        for c in children.values():
            print(c.index, end=',')
        print()


    def selection() -> Node:

        return Node()

    def expansion() -> None:
        pass




