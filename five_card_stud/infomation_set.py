class information_set():
    __slots__ = {
        "information", "last_info",
    }

    def __init__(self):
        self.information = ""
        self.last_info = ""

    def deepCopy(self):
        info = information_set()
        info.information = self.information
        info.last_info = self.last_info

    def encode_and_insert(self, is_card, player_index, value):
        '''
        Args:
            is_card: True if new information is a card, False otherwise
            player_index: index of player who get this card or take this action
            value: a card if new information if a card; othewise, action tuple
        '''
        new_info = self.encode_card(player_index, value) if is_card else self.encode_action(player_index, value)
        self.add_to_info_set(new_info)

    def add_to_info_set(self, new_info):
        if len(self.information) != 0:
            # Add deliminator
            if new_info[0] != self.last_info[0]:
                # between betting round and dealing round; or vice versa
                self.information += ';'
            else:
                self.information += ','
        self.information += new_info
        self.last_info = new_info

    def encode_card(self, player_index, card):
        prefix = "C"
        return '-'.join((prefix, str(player_index), str(card)))

    def encode_action(self, player_index, action_tup):
        prefix = 'A'
        return '-'.join((prefix, str(player_index), str(action_tup)))


    def decode(self):
        '''
        Decode the current info set to a list of
        '''
        pass