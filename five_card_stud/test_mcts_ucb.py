#########################################################
# Test the performance & efficiency of MCTS agents with 
# different itration numbers. We define:
# - Performance: the probability of win by playing with
#   uniform agent
# - Efficiency: the mean decision time each agent spent
#   throughout the whole game with uniform agent
#########################################################
from random import Random
from .gameState import GameState
from .agent import *
from .card import *
from .constants import debug
import time
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
from mctsAgent import MCTSAgent2
import numpy as np
import tqdm
from statistics import mean
sns.set()



def play_game(C, time_record):
    '''
    Return the winner index
    '''

    # Initialize game states
    game = GameState(balance=100)
    # Initialize players based on algorithm
    game.players = [MCTSAgent2(game.balance, 0, 0, True, n_iterations=100, C=C), 
                    RandomAgent(game.balance, 1, 0, True, False)]

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
                if player.index == 0:
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
    C_range = np.arange(1, 10)
    n_runs = 1000
    win_times = np.zeros(len(C_range)) # win times of MCTS Agent
    mean_time_record = np.zeros(len(C_range)) # win times of MCTS Agent
    for i in tqdm.tqdm(range(len(C_range))):
        # Time record for MCTS agent
        print("Test C=", C_range[i])
        time_record = []
        for _ in range(n_runs):
            winner = play_game(C=C_range[i], time_record=time_record)
            if winner == 0:
                win_times[i] += 1
        mean_time_record[i] = mean(time_record)

    print("win_times", win_times)
    print("mean_time_record", mean_time_record)
    plt.subplot(121)
    plt.title("Number of wins vs. C")
    plt.xlabel("C")
    plt.ylabel("Number of Wins")
    plt.plot(C_range, win_times)
    plt.subplot(122)
    plt.title("Average time of play vs. C")
    plt.xlabel("C")
    plt.ylabel("Average time of play")
    plt.plot(C_range, mean_time_record/1e9)
    plt.show()

if __name__ == "__main__":
    main()
