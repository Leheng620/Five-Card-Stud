class AbstractPlayer:
    def __init__(self, balance, index, cards, chip, alive):
        self.balance = balance
        self.index = index
        self.cards = cards
        self.revealed_cards = cards[1:]
        self.chip = chip
        self.alive = alive


class Agent(AbstractPlayer):

    def __init__(self, balance, index, cards, chip, alive):
        super(Agent, self).__init__(balance, index, cards, chip, alive)
