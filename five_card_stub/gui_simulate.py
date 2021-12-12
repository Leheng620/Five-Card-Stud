from constants import *
from card import *
import random
from gameState import GameState

def clear(player):
    players = player["showhand"]["players"]
    for p in players:
        if isinstance(p, dict):
            p["cards"] = []
            p["alive"] = True
            p["chip"] = 0
            p["endType"] = 0
    player["showhand"]["repeat"] = False
    player["showhand"]["chipCap"] = min([p["balance"] for p in players if isinstance(p, dict)])
    return player


def add_player(game, *args):
    num = int(args[0])
    name = args[1]
    agent = int(args[2]) # index of ["MCTS Agent", "Uniform Agent", "Random Agent"]
    num_iteration = int(args[3]) # for mcts
    players = game["players"]
    if players[num - 1] == 0:
        comp = {
            "pic": "./static/pic/dp.jpg",
            "agent": agent,  # agent type
            "balance": 100,
            "name": name,
            "iteration": num_iteration
        }
        players[num - 1] = comp
    else:
        players[num - 1]["name"] = name  # update player only
    game["chipCap"] = min([p["balance"] for p in players if isinstance(p, dict)])
    return game


def delete_player(game, *args):
    num = int(args[0])
    players = game["players"]
    players[num - 1] = 0
    player_balance = [p["balance"] for p in players if isinstance(p, dict)]
    game["maxChip"] = 0 if len(player_balance) == 0 else min(player_balance)
    return game


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

    game_state.initialize_game_state()

    game, game_state = update_game_state(game, game_state)

    return game, game_state

def begin(game):
    '''
    Begin the game, pay enter ticket, distribute 2 cards
    Simulate through player decision state
    :param player: the player object
    :param room_level: current room level
    :param args:
    :return: updated player object
    '''
    game, game_state = init_game_state(game)
    game, game_state = process_before_player(game, game_state)

    return game, game_state

def process_before_player(game, game_state):
    game_state.start_betting_round()

    while True:
        player = game_state.pop_get_next_player()
        if player.index == 4:
            game_state.player_queue.append_left(player)
            break
        else:
            player.play(game_state)

    return update_game_state(game, game_state)

def update_game_state(game, game_state):
    players = game["players"]

    for p in game_state.players:
        players[p.index].update(p.jsonify())

    game.update({
        "firstPlayer": game_state.first_player,
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
        player.save_selected_action(Actions.CALL, 0)
    elif option == 'player-add':
        player.save_selected_action(Actions.RAISE, int(args[1]))
    elif option == 'player-give-up':
        player.save_selected_action(Actions.FOLD, 0)
    else:
        player.save_selected_action(Actions.CHECK, 0)

    player.play(game)

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

def repeat_round(player, room_level, *args):
    player_objs = create_player_obj(player, room_level)
    player_objs = shift_player_object(player, player_objs)
    player["showhand"]["repeat"] = True
    process_before_player(player, player_objs, True)
    update_player(player, player_objs)
    return player

def next_round(game, game_state, *args):
    process_before_player(player, player_objs, False)
    update_player(player, player_objs)

    return player

def get_winner(player, room_level, *args):
    player_objs = create_player_obj(player, room_level)
    players_remain = [p for p in player_objs if p.alive]
    players = player["showhand"]["players"]
    if len(players_remain) > 1:
        players_remain.sort(key=cmp_five_cards, reverse=True)
        result = []
        for p in players_remain:
            result.append(cmp_five_cards(p, cards=p.cards))
        for i in range(len(players_remain)):
            index = players_remain[i].index
            players[index]["endType"] = card_type_map_cn[result[i][0]]
        player["showhand"]["firstPlayer"] = players_remain[0].index
    return player
