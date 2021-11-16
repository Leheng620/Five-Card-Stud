from gameState import GameState
from agent import *
from card import *


def main():
    game = GameState(algorithm="mcts")
    while True:
        game.print_cards()
        game.start_betting_round()

        while True:
            player = game.pop_get_next_player()
            player.play(game)
            print("[debug] total_chips:", game.total_chips, "current_max_chips:",game.current_max_chips,
                  "player:", player.index, "balance:", player.balance)
            if game.is_round_end():
                break
        game.end_betting_round()
        if game.is_game_end():
            print("winner: player %d" % game.get_winner())
            break
        else:
            game.deal()

if __name__ == "__main__":
    main()