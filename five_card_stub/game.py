from gameState import GameState
from agent import *
from card import *


def main(n_players=2, balance=100):
    game = GameState(n_players, balance)
    while(game.is_game_end() is False):
        game.deal()
        game.build_player_queue()
        while(game.is_round_end() is False):
            player = game.get_next_player()
            player.play(game)

        game.clear_player_queue()





if __name__ == "__main__":
    main()