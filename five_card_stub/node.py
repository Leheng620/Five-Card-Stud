from constants import NodeMeta
from math import sqrt, log

class Node:
    def __init__(self, action: tuple = None, parent: object = None):
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

    def add_children(self, children: dict) -> None:
        '''
        Mapping: action -> child
        '''
        for child in children:
            self.children[child.action] = child
    
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

    
