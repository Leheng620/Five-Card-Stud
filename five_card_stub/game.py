from gameState import GameState
from agent import *
from card import *
from collections import Counter
from constants import debug
import sys
import tqdm


def play_game(algorithm, MCTS_iterations=None):
    '''
    Return the winner index
    '''
    # Initialize game states
    game = GameState(balance=100)
    # Initialize players based on algorithm
    game.initializePlayers(algorithm, MCTS_iterations)

    game_count = 0
    while True:
        game_count += 1
        debug("*************************************************")
        debug("Game %d starts..." % game_count)
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
                game.print_all_player_balance()
                break
            else:
                game.deal()
        if game.is_terminal():
            break
    balances = [p.balance for p in game.players]
    return balances.index(max(balances))


def main(algorithm="mcts_vs_uniform", MCTS_iterations=100, debug_flag=0):
    Debug.debug = debug_flag
    winner_lst = []
    lst = [0, 0]
    for _ in tqdm.tqdm(range(1000)):
        winner = play_game(algorithm, MCTS_iterations)
        winner_lst.append(winner)
        lst[winner] += 1
    counter = Counter(winner_lst)
    print("Result of %s: " % algorithm)
    print("    Player 0 wins %d times," % counter[0])
    print("    Player 1 wins %d times," % counter[1])
    print("----------------%d games in total" % sum(counter.values()))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2 and sys.argv[1] == "random_vs_uniform":
        main(algorithm=sys.argv[1])
    elif len(sys.argv) == 3 and (sys.argv[1] == "mcts_vs_uniform" or sys.argv[1] == "mcts_vs_random" ):
        main(algorithm=sys.argv[1], MCTS_iterations=int(sys.argv[2]))
    elif len(sys.argv) == 4 and sys.argv[1] == "mcts_vs_mcts":
        MCTS_iterations = [int(sys.argv[2]), int(sys.argv[3])]
        main(algorithm=sys.argv[1], MCTS_iterations=MCTS_iterations)
    else:
        raise Exception("invalid arguments!")