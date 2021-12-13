####################################################
#
# Define a human agent what takes command line input
#
####################################################
from .agent import RandomAgent
from .constants import Actions


class HumanAgent(RandomAgent):
    def __init__(self, balance, index, chip, alive):
        super(HumanAgent, self).__init__(balance, index, chip, alive)
    
    def decide_action(self, game):
        allow_actions = game.get_allow_actions()
        print("*********************************")
        self.print_secret_card()
        print("Your balance is", self.balance)
        print("Please choose a action:")
        for i, action in enumerate(allow_actions):
            print("  %d - %s" % (i, action))
        index = int(input("Your choice: "))
        action = allow_actions[index]
        print("You choose to %s" % action)
        if action == Actions.RAISE:
            print("Please choose an amount of chips to RAISE:")
            raise_chip = int(input("Your choice: "))
            return (action, raise_chip)
        else:
            return (action, 0)
        

class HumanGUIAgent(RandomAgent):
    def __init__(self, balance, index, chip, alive):
        super(RandomAgent, self).__init__(balance, index, chip, alive)
        self.selected_action = None

    def save_selected_action(self, action_tup):
        self.selected_action = action_tup

    def decide_action(self, game):
        return self.selected_action

        
        

