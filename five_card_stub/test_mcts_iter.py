#########################################################
# Test the performance & efficiency of MCTS agents with 
# different itration numbers. We define:
# - Performance: the probability of win by playing with
#   uniform agent
# - Efficiency: the mean decision time each agent spent
#   throughout the whole game with uniform agent
#########################################################
from gameState import GameState
from agent import *
from card import *
from collections import Counter
from constants import debug
import time
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()


def play_game(algorithm, MCTS_iterations=None, time_record=None):
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
                # record time taken for MCTS agent to play
                if time_record != None and player.index == 0:
                    time_record.append(end - start)
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

def main(debug=0):
    Debug.debug = debug
    MCTS_iter_range = range(100, 1000, 100)
    n_runs = 100
    win_times = [0 for _ in range(len(MCTS_iter_range))] # win times of MCTS Agent
    mean_time_record = [0 for _ in range(len(MCTS_iter_range))] # win times of MCTS Agent
    for MCTS_iter in MCTS_iter_range:
        index = MCTS_iter // 100 - 1
        # Time record for MCTS agent
        time_record = [] 
        for _ in range(n_runs):
            winner = play_game(algorithm="mcts_vs_uniform", MCTS_iterations=MCTS_iter, time_record=time_record)
            if winner == 0:
                win_times[index] += 1
        mean_time_record[index] = mean(time_record)

    print("win_times", win_times)
    print("mean_time_record", mean_time_record)
    plt.subplot(121)
    plt.title("Number of wins vs. iteration number")
    plt.xlabel("Iteration Number")
    plt.ylabel("Number of Wins")
    plt.plot(MCTS_iter_range, win_times)
    plt.subplot(122)
    plt.title("Average time of play vs. iteration number")
    plt.xlabel("Iteration Number")
    plt.ylabel("Average time of play")
    plt.plot(MCTS_iter_range, mean_time_record)
    plt.show()

if __name__ == "__main__":
    main()
