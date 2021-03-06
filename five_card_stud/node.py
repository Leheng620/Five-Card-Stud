from math import sqrt, log
import random
from constants import INF

class Node:
    __slots__ = [
        'node_id', 
        'player_id',
        'action',
        'parent',
        'N',
        'U',
        'children',
        'outcome',
        'actions_not_expanded',
        'C']
        
    def __init__(self, node_id, action=None, parent=None, player_id=None, C=sqrt(2)):
        '''
        Args:
            action:     the action taken at the parent node (which leads to this node)
            parent:     parent node
            N:          exploration count, the number of simulations that was applied to this node
            U:          the number of wins during past simulations 
            children:   children of this node; will be added when this node is expanded in Monte-Carlo Tree
            outcome:    the winner of this node when the node is a leaf node; otherwise, None
            state:      game state of the current node
        '''
        self.node_id = node_id
        self.player_id = player_id
        self.action = action
        self.parent = parent
        self.N = 0
        self.U = 0
        self.children = {}  
        self.outcome = None
        self.actions_not_expanded = None
        self.C = C

    def set_player_id(self, id):
        self.player_id = id

    def get_action_to_expand(self):
        '''
        Return a ramdom unexpanded action
        '''
        action = random.choice(self.actions_not_expanded)
        self.actions_not_expanded.remove(action)
        return action


    def add_child(self, action, child) -> None:
        '''
        Append to self.children
        '''
        self.children[action] = child

    
    @property
    def value(self) -> float:
        '''
        Calculate the UCB1 value of this node
        '''
        if self.parent is None:
            raise Exception("Computation of UCB1 failed, parent is None");
        
        if self.N == 0:
            return INF
        else:
            return self.U / self.N + self.C * sqrt(log(self.parent.N) / self.N)

    