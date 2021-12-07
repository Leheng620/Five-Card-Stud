from agent import RandomAgent
from constants import Actions, NodeMeta, add_chip_amount, not_call_probability, not_raise_probability,\
    make_decision_using_probability, debug
from node import Node
from card import cmp_two_cards, cmp_three_cards, cmp_four_cards, cmp_five_cards, create_half_deck
import numpy as np
import random
from math import sqrt

CARD_DECK = create_half_deck()
class MCTSAgent(RandomAgent):
    def __init__(self, balance=100, index=0, chip=0, alive=True, n_iterations=100, C=sqrt(2)):
        '''
        Args:
            root_state:  the game state before each betting round
        '''
        super().__init__(balance, index, chip, alive)
        self.root_state = None
        self.root_node = None
        self.node_count = 0   # The number of node in the tree
        self.n_iterations = n_iterations
        self.C = C
    
    def deepCopy(self):
        '''
        Deepcopy the player object
        '''
        state = MCTSAgent(self.balance, self.index, self.chip, self.alive, C=self.C)
        state.cards = [card.copy() for card in self.cards]
        state.revealed_cards = state.cards[1:]
        state.__secret_card = state.cards[0]
        return state
        
    def decide_action(self, game):
        # if game.round < 4: return Actions.CHECK, 0
        self.root_state = game.deepCopy()                            # Deepcopy the current game state
        self.root_node = Node(self.node_count, None, None, self.index, C=self.C)      # Root Node: current game state
        self.node_count = 0
        for _ in range(self.n_iterations):
            # Keep selecting best child node until the leaf node
            leaf, state = self.selection()
            # print("[SELECTION] node: %d" % leaf.node_id)

            # Expand the game tree, appending all child nodes
            child = self.expansion(leaf, state)

            # Simulate at an arbitrary child of node
            winner_id = self.simulation(child, state)

            # Back-propogate from child to root
            self.back_propagate(winner_id, child)

        # for child in self.root_node.children.values():
        #     debug(child.node_id, child.action, child.N, child.U)
        values = [child.value for child in self.root_node.children.values()]
        child = random.choice([child for child in self.root_node.children.values() if child.value == max(values)])
        action = child.action
        raise_chip = 10 if action == Actions.RAISE else 0
        raise_chip = calculate_prob_weight_given_actions(self.root_state.get_current_player(),
                                                         [action], self.root_state)[1]

        return action, raise_chip

    def check_game_state_and_act(self, state, action):
        '''
        Return True if game ends;
        Else, let the current player act and return False
        '''
        if state.is_round_end():
            state.end_betting_round()
            if state.is_game_end():
                # Game ends, child is a leaf node
                return
            else:
                # Game continues, deal cards and start next betting round
                state.deal()
                state.start_betting_round()
        
        player = state.get_current_player()
        raise_amount = calculate_prob_weight_given_actions(player, [action], state)[1]
        action_tup = (action, raise_amount)
        player.act(state, action_tup)
        state.pop_get_next_player()

    def selection(self):
        '''
        Return a leaf node
        '''
        state = self.root_state.deepCopy()
        node = self.root_node
        while len(node.children) > 0:
            values = [child.value for child in node.children.values()]
            node = random.choice([child for child in node.children.values() if child.value == max(values)])
            self.check_game_state_and_act(state, node.action)
        return node, state

    def expansion(self, node, state):
        '''
        Append all the child of node
        If node is a terminal node, return node itself; otherwise, return a random child of node
        '''
        if state.is_round_end():
            state.end_betting_round()
            if state.is_game_end():
                # Game ends, child is a leaf node
                winner = state.get_winner()
                node.outcome = winner
                return node
            else:
                # Game continues, deal cards and start next betting round
                state.deal()
                state.start_betting_round()

        if node.actions_not_expanded is None:
            node.actions_not_expanded = state.get_allow_actions()
            for action in node.actions_not_expanded:
                child = Node(self.node_count, action, node, C=self.C)
                child.set_player_id(state.get_next_player().index)
                self.node_count += 1
                node.add_child(action, child)

        action = node.get_action_to_expand()

        raise_amount = calculate_prob_weight_given_actions(state.get_current_player(), [action], state)[1]
        action_tup = (action, raise_amount)
        curr_player = state.get_current_player()
        curr_player.act(state, action_tup)
        next_player = state.pop_get_next_player()
        # node.children[action].set_player_id(next_player.index)
        
        return node.children[action]

    def simulation(self, node, state) -> int:
        '''
        Simulate from node till the game ends
        Return the result (winner id)
        '''
        while True:
            if state.is_round_end():
                state.end_betting_round()
                if state.is_game_end():
                    # Game ends, child is a leaf node
                    winner = state.get_winner()
                    node.outcome = winner
                    # print("***[Game End] winner: %d" % winner)
                    return winner
                else:
                    # Game continues, deal cards and start next betting round
                    state.deal()
                    state.start_betting_round()
                    # print("***[Round End] round: %d" % state.round)

            allow_actions = state.get_allow_actions()
            weights, raise_amount = calculate_prob_weight_given_actions(state.get_current_player(), allow_actions, state)
            action = random.choice(state.get_allow_actions()) # Choose a random action
            raise_amount = 0 if action == Actions.CHECK or action == Actions.FOLD or action == Actions.CALL else raise_amount
            action_tup = (action, raise_amount)


            curr_player = state.get_current_player()
            curr_player.act(state, action_tup)
            state.pop_get_next_player()        
    
    def back_propagate(self, winner_id, leaf):
        node = leaf
        while node is not None:
            node.N += 1
            if node.parent is not None and node.parent.player_id == winner_id:
                node.U += 1
            node = node.parent
        

    # def build_tree(self, state, node):
    #     allow_actions = state.get_allow_actions()
        
    #     print("-------------------------------------------------------")
    #     print("[Expand] node:", node.node_id, ", player:", node.player_id, ", allow_actions:", allow_actions)
    #     for action in allow_actions:
    #         # Update state: next_player act
    #         new_state = deepcopy(state)       # next_player will act on a copy of the current state
    #         action_tup = (action, 10 if action == Actions.RAISE else 0)
    #         curr_player = new_state.get_current_player()
    #         curr_player.act(new_state, action_tup)
    #         next_player = new_state.pop_get_next_player()
    #         self.node_count += 1
    #         child = Node(self.node_count, next_player.index, new_state, action, node)
    #         node.add_child(action, child)
    #         print("[New Child] parent:", node.node_id, ", action:", action, ", child:", child.node_id)


    #         if new_state.is_round_end():
    #             if new_state.is_game_end():
    #                 # Game ends, child is a leaf node
    #                 winner = new_state.get_winner()
    #                 child.outcome = winner
    #                 print("***[Game End] node: %d, winner: player %d" % (child.node_id, winner))
    #             else:
    #                 # Game continues, directly enter next betting round and build tree
    #                 child.mark_deal_needed()  # Mark deal is needed at this node in simulation
    #                 print("***[Round End] node: %d" % (child.node_id))
    #         else:
    #             self.build_tree(new_state, child)
            
    #         print()

def calculate_prob_weight_given_actions(player, actions, state):
    # if len(actions) == 1:
    #     return [1], 0
    weights = np.zeros((len(actions),))
    raise_amount = state.ante
    players_remain = [p for p in state.get_alive_players() if p != player]
    highest_chip = max([i.chip for i in players_remain])
    card_deck = create_remaining_card_deck(player, [i for i in state.players if i != player])
    losing_prob = calculate_losing_prob(player, players_remain, card_deck)
    cost_percentage = highest_chip / state.max_chips
    balance_percentage = highest_chip / (player.balance + player.chip)

    for i, action in enumerate(actions):
        if action == Actions.RAISE:
            prob_table = not_raise_probability[len(player.cards)]
            not_raise_prob = prob_table[0] * losing_prob + prob_table[1] * cost_percentage + prob_table[
                2] * balance_percentage
            raise_prob = 1 - not_raise_prob
            chip_remains = state.max_chips - highest_chip
            raise_amount = handle_add_chip(player, losing_prob, chip_remains)
            weights[i] = raise_prob
        elif action == Actions.CHECK:
            prob_table = not_raise_probability[len(player.cards)]
            not_raise_prob = prob_table[0] * losing_prob + prob_table[1] * cost_percentage + prob_table[
                2] * balance_percentage
            weights[i] = not_raise_prob
        elif action == Actions.CALL:
            prob_table = not_call_probability[len(player.cards)]
            not_call_prob = prob_table[0] * losing_prob + prob_table[1] * cost_percentage + prob_table[
                2] * balance_percentage
            call_prob = 1 - not_call_prob
            weights[i] = call_prob
        elif action == Actions.FOLD:
            prob_table = not_call_probability[len(player.cards)]
            not_call_prob = prob_table[0] * losing_prob + prob_table[1] * cost_percentage + prob_table[
                2] * balance_percentage
            weights[i] = not_call_prob
        else:
            weights[i] = (1-losing_prob) * add_chip_amount[len(player.cards)][2]
            raise_amount = state.max_chips - player.chip
    weights *= 100
    weights = weights.astype(dtype=int)

    return weights.tolist(), raise_amount



def calculate_losing_prob(player, other_players_objs, card_deck):
    num_of_cards = len(player.cards)
    calling_func = {2: cmp_two_cards, 3: cmp_three_cards, 4: cmp_four_cards, 5: cmp_five_cards}
    self_card_type = calling_func[num_of_cards](player, cards=player.cards)
    max_losing_prob = 0
    for player_obj in other_players_objs:
        possibility = []  # possible type
        for card in card_deck:
            player_cards = player_obj.revealed_cards + [card]
            possibility.append(calling_func[num_of_cards](player_obj, cards=player_cards))
        possibility.sort(reverse=True)
        count = 0
        for p in possibility:
            if p < self_card_type:
                break
            count += 1
        prob = count / len(possibility)  # # larger than self / total
        max_losing_prob = max(max_losing_prob, prob)
    return max_losing_prob

def handle_add_chip(player, losing_prob, remain_chip_total):
    showhand_prob = (1-losing_prob) * add_chip_amount[len(player.cards)][2]
    if make_decision_using_probability(showhand_prob):
        return remain_chip_total
    no_factor_prob = add_chip_amount[len(player.cards)][0]
    if make_decision_using_probability(no_factor_prob):
        return int((1-losing_prob) * remain_chip_total)
    return int(add_chip_amount[len(player.cards)][1] * (1-losing_prob) * remain_chip_total)

def create_remaining_card_deck(player, other_players_objs):
    cards_on_table = [j for i in other_players_objs for j in i.revealed_cards] + player.cards
    cards_on_table_set = set(cards_on_table)
    cards = []
    # a little stupid O(mn) algor, worse case for half deck m = 24, n = 24,
    #  use sort() to speed up if necessary
    for card in CARD_DECK:
        if not card in cards_on_table_set:
            cards.append(card)
    return cards

        
