from gameState import GameState
from agent import *
from card import *


def main():
    game = GameState()
    while True:
        game.print_cards()
        game.build_player_queue()
        while True:
            player = game.get_next_player()
            player.play(game)
            print("total_chips:", game.total_chips, "player:", player.index, "balance:", player.balance)
            if game.is_round_end():
                break
        game.clear_player_queue()
        if game.is_game_end():
            break
        else:
            game.deal()

if __name__ == "__main__":
    main()