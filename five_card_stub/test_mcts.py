# Test one player act based on Monte-Carlo Tree Search
from gameState import GameState
from card import *


def main():
    game = GameState(algorithm="mcts")
    game.print_cards()
    game.build_player_queue()

    repeat = False
    player = game.get_next_player()
    player.play(game, repeat)
    print("[debug] total_chips:", game.total_chips, "current_max_chips:",game.current_max_chips,
            "player:", player.index, "balance:", player.balance)
           

if __name__ == "__main__":
    main()