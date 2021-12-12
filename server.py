from flask import Flask, render_template, request, jsonify, redirect
import json, os
from five_card_stub.constants import *
from five_card_stub.gui_simulate import *

app = Flask(__name__)

game = None  # current game state in json version
room_level = 0 # the current room level
game_state = None # current gameState object

command_control = {
    'add-player': add_player,
    'delete-player': delete_player,
    'begin': begin,
    'process-player-option': process_player_option,
    'repeat-round': repeat_round,
    'next-round': next_round,
    'get-winner': get_winner
}

def load_init_game_state():
    # there is only one human player
    game_state_before_game_start = {
        "players": [0, 0, 0, 0, {
            "pic": "./static/pic/dp.jpg",
            "balance": 100,
            "name": "hi",
            "agent": 4,
            "iteration": 0
        }, 0],
        "maxChip": 100
    }
    # cannot use str() blc front end will not receive response
    return game_state_before_game_start

def load_player():
    game_state_before_game_start = {
        "players": [0, 0, 0, 0, 0, 0],
        "firstPlayer": 0,
        "maxChip": 0,
        "totalChip": 0,
        "currentMaxChip": 0,
        "repeat": False,
        "endType": 0
    }
    # cannot use str() blc front end will not receive response
    return game_state_before_game_start

def update_game(g, gs):
    global game, game_state
    game, game_state= g, gs

def get_dict_str(p):
    return jsonify(game=p)


@app.route('/')
def five_card_stud():
    return render_template('index.html')


@app.route('/fcsmsg', methods=['POST'])
def fcs_msg():
    data = json.loads(request.get_data())
    print(data)
    global game, game_state
    if data['command'] == 'init':
        return_val = load_init_game_state()
        update_game(return_val, None)
        return_val = get_dict_str(return_val)
    elif data['command'] == 'load-player':
        # return_val = sh.clear(game)
        # update_game(return_val)
        # return_val = get_dict_str(return_val)
        pass
    else:
        return_game, return_game_state = command_control[data['command']](game, *data['args'])
        update_game(return_game, return_game_state)
        return_val = get_dict_str(return_game)
    print(game)
    return return_val


if __name__ == '__main__':
    app.run(port=5001)
