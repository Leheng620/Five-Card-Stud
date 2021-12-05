from gameState import GameState
from agent import *
from card import *
from collections import Counter
from constants import debug


def play_game(t):
    '''
    Return the winner index
    '''
    game = GameState(algorithm="compare", balance=50)
    game_count = 0
    while True:
        game_count += 1
        # print("*************************************************")
        # print("Game %d starts..." % game_count)
        game.initialize_game_state()

        while True:
            # game.print_cards()
            game.start_betting_round()

            while True:
                player = game.pop_get_next_player()
                player.play(game)
                debug("total_chips:", game.total_chips, "current_max_chips:",game.current_max_chips,
                    "player:", player.index, "balance:", player.balance)
                if game.is_round_end():
                    break
            game.end_betting_round()
            if game.is_game_end():
                debug("player %d wins %d chips!" % (game.get_winner(), game.total_chips))
                game.checkout()
                # game.print_results()
                break
            else:
                game.deal()
        if game.is_terminal():
            break
    balances = [p.balance for p in game.players]
    return balances.index(max(balances))

def main(debug=0):
    Debug.debug = debug
    winner_lst = []
    for i in range(1000):
        winner = play_game()
        winner_lst.append(winner)
        if i % 10 == 0:
            print(Counter(winner_lst))

    counter = Counter(winner_lst)
    print(counter)

if __name__ == "__main__":
    main()