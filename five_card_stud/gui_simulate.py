from .constants import *
from .card import *
import random
from .gameState import GameState

def clear(game, game_state):
    game_state.checkout()
    if game_state.is_terminal():
        game["terminal"] = True
    players = game["players"]
    game, game_state = update_game_state(game, game_state)
    game["maxChip"] = min([p["balance"] for p in players if isinstance(p, dict)])
    return game, game_state


def add_player(game, game_state, *args):
    num = int(args[0])
    name = args[1]
    agent = int(args[2]) # index of ["MCTS Agent", "Uniform Agent", "Random Agent"]
    num_iteration = int(args[3]) # for mcts
    players = game["players"]
    pic_map = {1: "./static/pic/mcts.png", 2: "./static/pic/uniform.png", 3: "./static/pic/random.png"}
    if players[num - 1] == 0:
        comp = {
            "pic": pic_map[agent],
            "agent": agent,  # agent type
            "balance": 100,
            "name": name,
            "iteration": num_iteration,
            "alive": True
        }
        players[num - 1] = comp
    else:
        players[num - 1]["iteration"] = num_iteration
        players[num - 1]["agent"] = agent
        players[num - 1]["pic"] = pic_map[agent]
        players[num - 1]["name"] = name  # update player only
    game["maxChip"] = min([p["balance"] for p in players if isinstance(p, dict)])
    return game, None


def delete_player(game, game_state, *args):
    num = int(args[0])
    players = game["players"]
    players[num - 1] = 0
    player_balance = [p["balance"] for p in players if isinstance(p, dict)]
    game["maxChip"] = 0 if len(player_balance) == 0 else min(player_balance)
    return game, None


def init_game_state(game):
    '''
    Create gameState object
    :param game: a dictionary version of gameState object, will be sent to front end
    :return:
    '''
    players = game["players"]
    player_index = [p for p in range(len(players)) if isinstance(players[p], dict)]
    num_players = len([p for p in players if isinstance(p, dict)])
    algorithm = [(p["agent"], p["iteration"]) for p in players if isinstance(p, dict)]
    game_state = GameState(balance=100, n_players=num_players)
    game_state.initializePlayers(algorithm=algorithm)
    for i in range(num_players):
        game_state.players[i].index = player_index[i] # reset index for front end display

    game, game_state = update_game_state(game, game_state)

    return game, game_state

def begin(game, game_state):
    '''
    Begin the game, pay enter ticket, distribute 2 cards
    Simulate through player decision state
    :param player: the player object
    :param room_level: current room level
    :param args:
    :return: updated player object
    '''
    if game_state is None:
        game, game_state = init_game_state(game)

    game_state.initialize_game_state()
    game, game_state = process_before_player(game, game_state, False)

    return game, game_state

def process_before_player(game, game_state, repeat):
    if not repeat:
        game_state.start_betting_round()

    while True:
        next_player = game_state.get_next_player()
        if next_player.index == 4:
            break
        else:
            player = game_state.pop_get_next_player()
            player.play(game_state)

    return update_game_state(game, game_state)

def update_game_state(game, game_state):
    players = game["players"]

    for p in game_state.players:
        players[p.index].update(p.jsonify())

    game.update({
        "firstPlayer": game_state.table_index,
        "maxChip": game_state.max_chips,
        "totalChip": game_state.total_chips,
        "currentMaxChip": game_state.current_max_chips,
        "repeat": game_state.repeat,
        "endType": 0
    })
    return game, game_state

def process_player_option(game, game_state, *args):
    player = game_state.pop_get_next_player()
    option = args[0]
    if option == 'player-follow':
        player.save_selected_action((Actions.CALL, 0))
    elif option == 'player-add':
        player.save_selected_action((Actions.RAISE, int(args[1])))
    elif option == 'player-give-up':
        player.save_selected_action((Actions.FOLD, 0))
    else:
        player.save_selected_action((Actions.CHECK, 0))

    player.play(game_state)

    return process_after_player(game, game_state, game_state.repeat)


def process_after_player(game, game_state, repeat):
    while True:
        if game_state.is_round_end():
            break
        elif game_state.repeat == True and repeat == False:
            break
        player = game_state.pop_get_next_player()
        player.play(game_state)

    return update_game_state(game, game_state)

def num_players_alive(player_objs):
    return len([p for p in player_objs if p.alive])

def repeat_round(game, game_state):
    return process_before_player(game, game_state, True)


def next_round(game, game_state, *args):
    game_state.end_betting_round()
    game_state.deal()
    return process_before_player(game, game_state, False)

def get_winner(game, game_state, *args):
    alive_player = game_state.get_alive_players()
    if len(alive_player) > 1:
        for player_obj in alive_player:
            table_index = player_obj.index # the index of the table where the player sits in front end
            game["players"][table_index]["endType"] = card_type_map_cn[cmp_five_cards(player_obj, cards=player_obj.cards)[0]]
    game, game_state = update_game_state(game, game_state)
    game["firstPlayer"] = game_state.players[game_state.get_winner()].index
    return game, game_state
