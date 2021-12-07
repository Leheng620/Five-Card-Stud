#########################################################
# Test the efficiency of multiple agents:
# - Uniform Agent
# - Random Heuristic Agent
# - MCTS Agent
#########################################################
from gameState import GameState
from agent import *
from card import *
from collections import Counter
from constants import debug
import time
import sys
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns
import math
sns.set()

# Time record for each player's play phase
time_record = [[[] for _ in range(4)] for _ in range(2)] 

def get_log(x, base):
    return math.log(x, base) if x > 0 else 0


def play_game(algorithm, MCTS_iterations=None):
    '''
    Return the winner index
    '''

    # Initialize game states
    game = GameState(balance=100)
    # Initialize players based on algorithm
    game.initializePlayers(algorithm=algorithm, MCTS_iterations=MCTS_iterations)

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
                
                start = time.time_ns()
                player.play(game)
                end = time.time_ns()
                time_record[player.index][game.round-1].append(end - start)
                debug("total_chips:", game.total_chips, "current_max_chips:",game.current_max_chips,
                    "player:", player.index, "balance:", player.balance)
                if game.is_round_end():
                    break
            game.end_betting_round()
            if game.is_game_end():
                debug("player %d wins %d chips!" % (game.get_winner(), game.total_chips))
                game.checkout()
                # game.print_all_player_balance()
                break
            else:
                game.deal()
        if game.is_terminal():
            break
    balances = [p.balance for p in game.players]
    return balances.index(max(balances))

def main(algorithm="mcts_vs_uniform", MCTS_iterations=100, debug=0):
    Debug.debug = debug
    winner_lst = []
    for _ in range(100):
        winner = play_game(algorithm, MCTS_iterations)
        winner_lst.append(winner)

    counter = Counter(winner_lst)
    print(counter)

    avg_time_record = [[mean(round_time_record)/1000 + 1 for round_time_record in time_record[i]] for i in range(2)]
    print(avg_time_record)
    plt.title("Mean play time (MCTS Agent with n_iter=100 vs. Uniform Agent)")
    plt.xlabel("Round")
    plt.ylabel("Time (microseconds)")
    plt.yscale("log")
    plt.plot(range(1, 5), avg_time_record[0], label="MCTS Agent with n_iter=100")
    plt.plot(range(1, 5), avg_time_record[1], label="Uniform Agent")
    plt.legend()
    plt.show()

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