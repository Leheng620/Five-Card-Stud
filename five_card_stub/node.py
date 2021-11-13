class Node():
    def __init__(self, children=None, parent=None, win_cnt=0, expl_cnt=0):
        self.children = children
        self.parent = parent
        self.win_cnt = win_cnt
        self.expl_cnt = expl_cnt