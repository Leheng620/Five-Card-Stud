import card
from constants import debug, Debug, TWENTY_EIGHT_CHOOSE_FIVE, CHANCE_NODE
from collections import Counter
import pickle
import os


def binary_search(low, high, compare):
    '''
    Bounds: [low, high)
    :param low: lower bound
    :param high: upper bound
    :param compare: Compare function compare(index) that is used to compare between elements,
    should return positive integer/0/negative integer for greater/equal/less than the target.
    :param left_bound: True if there are multiple targets, choose the leftmost one, False otherwise.
    :return: The target between [low, high)
    '''
    upper_bound = high
    while(low < high):
        mid = low + (high-low) // 2
        if compare(mid) == 0:
            return mid
        elif compare(mid) > 0:
            high = mid
        elif compare(mid) < 0:
            low = mid + 1

    if low == upper_bound:
        low -= 1
    if compare(low) == 0:
        return low
    return -1


def backtrack(cards, card_deck, card_type_list, target_len):
    '''
    calculate the combinations of card_deck.
    :param cards: The cards already been picked
    :param card_deck: The remaining cards to be picked
    :param card_type_list: list of cards type
    :param target_len: len of each combination
    :return:
    '''
    if len(cards) == target_len:
        card_type_list.append(cards.copy())
    else:
        # [1, 2, 3, 4, 5, 6, 7] if target_len == 5
        # [1, 2, 3, 4, 5], [1, 2, 3, 4, 6], [1, 2, 3, 4, 7], [1, 2, 3, 5, 6], [1, 2, 3, 5, 7] ...
        # pick all the cards from card_deck as candidates until the last i cards
        # (if (target_len-1)-i cards have already been picked)
        for index, c in enumerate(card_deck[:len(card_deck) - (target_len - 1) + len(cards)]):
            cards.append(c)  # pick the card and backtrack
            cd = card_deck[index + 1:]  # remove this card from the deck
            backtrack(cards, cd, card_type_list, target_len)
            cards.pop()  # remove the picked card after backtrack, will pick another card in the next iteration


def find_all_combinations():
    '''
    Find all card types by calculating the combinations of 5 cards out of 28 cards. (28 choose 5)
    Then sort these combinations by card type
    :return: a sorted list of cards type
    '''

    all_card_type = []
    card_deck = card.create_half_deck()
    backtrack([], card_deck, all_card_type, 5)
    all_card_type.sort(key=lambda cy: card.cmp_five_cards(None, cards=cy))
    return all_card_type


def calculate_win_rate(all_card_type):
    '''
    calculate average win rate for 2, 3, 4, 5 cards on hand, and save them on disk
    :param all_card_type: return from find_all_combinations()
    '''

    def compare(i):
        '''
        compare function for binary search, card.cmp_five_cards can map card type into tuple
        :param t:
        :return:
        '''
        t1 = card.cmp_five_cards(None, all_card_type[i])
        t2 = card.cmp_five_cards(None, target)

        if t1[0] - t2[0] != 0:
            return t1[0] - t2[0]
        if t1[1] - t2[1] != 0:
            return t1[1] - t2[1]
        return t1[2] - t2[2]

    two_cards_win_rate = Counter()
    three_cards_win_rate = Counter()
    four_cards_win_rate = Counter()
    five_cards_win_rate = Counter()

    # need this to do the average
    two_cards_win_rate_count = Counter()
    three_cards_win_rate_count = Counter()
    four_cards_win_rate_count = Counter()
    five_cards_win_rate_count = Counter()

    wr_list = [two_cards_win_rate, three_cards_win_rate, four_cards_win_rate, five_cards_win_rate]
    wr_count_list = [two_cards_win_rate_count, three_cards_win_rate_count, four_cards_win_rate_count, five_cards_win_rate_count]

    for ct in all_card_type:
        target = ct
        win_rate = binary_search(0, len(all_card_type), compare) # find the position of this card type in all_card_type
        win_rate /= (len(all_card_type) - 1)
        for card_num, (wr, wr_count) in enumerate(zip(wr_list, wr_count_list)):
            num = card_num + 2
            combinations = []
            # calculate combinations of 2 cards. [8, 9, 10, J, Q] -> [[8, 9], [8, 10], [8, J]....]
            backtrack([], ct, combinations, num)
            for combination in combinations:
                key = "".join([str(c) for c in combination]) # make key as string repr of cards
                wr[key] += win_rate
                wr_count[key] += 1

    for (wr, wr_count) in zip(wr_list, wr_count_list):
        # take the average win rate two_cards, three_cards...
        for wr_key, wr_count_key in zip(wr.keys(), wr_count.keys()):
            wr[wr_key] /= wr_count[wr_count_key]

    with open(os.path.join(CHANCE_NODE, "2_cards_win_rate.obj"), 'wb') as f:
        pickle.dump(two_cards_win_rate, f)
    with open(os.path.join(CHANCE_NODE, "3_cards_win_rate.obj"), 'wb') as f:
        pickle.dump(three_cards_win_rate, f)
    with open(os.path.join(CHANCE_NODE, "4_cards_win_rate.obj"), 'wb') as f:
        pickle.dump(four_cards_win_rate, f)
    with open(os.path.join(CHANCE_NODE, "5_cards_win_rate.obj"), 'wb') as f:
        pickle.dump(five_cards_win_rate, f)


def load_win_rate():
    with open(os.path.join(CHANCE_NODE, "2_cards_win_rate.obj"), 'rb') as f:
        two_cards_win_rate = pickle.load(f)
    with open(os.path.join(CHANCE_NODE, "3_cards_win_rate.obj"), 'rb') as f:
        three_cards_win_rate = pickle.load(f)
    with open(os.path.join(CHANCE_NODE, "4_cards_win_rate.obj"), 'rb') as f:
        four_cards_win_rate = pickle.load(f)
    with open(os.path.join(CHANCE_NODE, "5_cards_win_rate.obj"), 'rb') as f:
        five_cards_win_rate = pickle.load(f)

    debug((two_cards_win_rate))
    # debug((four_cards_win_rate['♣10♣J♣Q♣K']))
    # debug(len(five_cards_win_rate))

def main(debug_flag=1):
    Debug.debug = debug_flag

    if not os.path.isdir(CHANCE_NODE):
        os.mkdir(CHANCE_NODE)
    if not os.path.isfile(os.path.join(CHANCE_NODE, '2_cards_win_rate.obj')):
        card_type_combinations = find_all_combinations()
        assert len(card_type_combinations) == TWENTY_EIGHT_CHOOSE_FIVE, "number of combinations mismatch"

        debug([str(i) for i in card_type_combinations[-1]])
        debug([str(i) for i in card_type_combinations[0]])

        calculate_win_rate(card_type_combinations)

    load_win_rate()


if __name__ == '__main__':
    main(1)
