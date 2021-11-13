from constants import NodeMeta, Action
from math import sqrt, log

class Node:
    def __init__(self, action: Action = None, parent: object = None, raise_limit = NodeMeta.RAISE_LIMIT, index=0, consecutive_checks=0):
        '''
        Args:
            action:     the action taken at the parent node (which leads to this node)
            parent:     parent node
            N:          exploration count, the number of simulations that was applied to this node
            U:          the number of wins during past simulations 
            children:   the children mapping: action -> child
            outcome:    the winner of this node when the node is a leaf node; otherwise, None
        '''
        self.action = action
        self.parent = parent
        self.N = 0
        self.U = 0
        self.children = {}
        self.outcome = None
        self.raise_limit = raise_limit
        self.index = index
        self.consecutive_checks = consecutive_checks

    def add_children(self, children: dict) -> None:
        '''
        children: dict that maps action to child
        '''
        for action, child in children.items():
            self.children[action] = child
    
    @property
    def value(self) -> float:
        '''
        Calculate the UCB1 value of this node
        '''
        if self.parent is None:
            raise Exception("Computation of UCB1 failed, parent is None");
        
        if self.N == 0:
            return NodeMeta.INF
        else:
            return self.U / self.N + NodeMeta.C * sqrt(log(self.parent.N) / self.N)

    