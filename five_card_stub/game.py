from gameState import GameState
from agent import *
from card import *


def main():
    game = GameState()
    while True:
        game.print_cards()
        game.build_player_queue()
        num_alive_players_been_processed = len(game.alive_indices)

        # when repeat is True, every player has made an action, and all players has either raised or checked once, then
        # the only action left for them is either fold or call. The idea is that every player can only make up to
        # 2 actions in a single round
        repeat = False
        while True:
            player = game.get_next_player()
            player.play(game, repeat)
            print("[debug] total_chips:", game.total_chips, "current_max_chips:",game.current_max_chips,
                  "player:", player.index, "balance:", player.balance)
            num_alive_players_been_processed -= 1
            if len(game.get_alive_players()) < 2:
                break
            elif num_alive_players_been_processed > 0 and repeat:
                if game.is_round_end(): # if all players have the current max chips on table, round end
                    break
            elif num_alive_players_been_processed == 0 and repeat:
                break
            elif num_alive_players_been_processed == 0 and not repeat:
                if game.is_round_end():
                    break
                else:
                    repeat = True
                    num_alive_players_been_processed = len(game.alive_indices)
        game.clear_player_queue()
        if game.is_game_end():
            print("winner: player %d" % game.get_winner())
            break
        else:
            game.deal()

if __name__ == "__main__":
    main()