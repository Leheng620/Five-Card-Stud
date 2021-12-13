from humanAgent import HumanAgent
from mctsAgent import MCTSAgent2
from gameState import GameState
from agent import *
from card import *
from collections import Counter
from constants import debug
import sys


def play_game(MCTS_iterations=100):
    '''
    Return the winner index
    '''
    # Initialize game states
    game = GameState(balance=100)
    # Initialize players based on algorithm
    game.players = [HumanAgent(game.balance, 0, 0, True), 
                    MCTSAgent2(game.balance, 1, 0, True, n_iterations=MCTS_iterations)]


    game_count = 0
    while True:
        game_count += 1
        debug("*************************************************")
        debug("Game %d starts..." % game_count)
        game.initialize_game_state()

        while True:
            game.print_revealed_cards()
            game.start_betting_round()

            while True:
                player = game.pop_get_next_player()
                player.play(game)
                if game.is_round_end():
                    break
            game.end_betting_round()
            debug("[Round End] total_chips:", game.total_chips, "current_max_chips:",game.current_max_chips)
            game.print_all_player_balance()
            if game.is_game_end():
                debug("[Game End] Player %d wins %d chips!" % (game.get_winner(), game.total_chips))
                if game.get_winner() == 0:
                    print("Congratulation! You win")
                game.print_cards()
                game.checkout()
                game.print_all_player_balance()
                break
            else:
                game.deal()
        if game.is_terminal():
            break
    balances = [p.balance for p in game.players]
    return balances.index(max(balances))


def main(MCTS_iterations=None, debug_flag=0):
    Debug.debug = debug_flag
    winner_lst = []
    for _ in range(10):
        winner = play_game()
        winner_lst.append(winner)

    counter = Counter(winner_lst)
    print(counter)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(MCTS_iterations=int(sys.argv[1]), debug_flag=1)
    else:
        main(debug_flag=1)
        



