import flask
from flask import request

import pickle
from lib.players import players_for_online

blueprint = flask.Blueprint(
    'players_api',
    __name__,
    template_folder='templates'
)

currentPlayer = 0
players = players_for_online.copy()


@blueprint.route('/game/<int:player_id>', methods=['POST'])
def send(player_id):
    if str(player_id) == "1":
        players[0] = pickle.loads(request.data)
        reply = pickle.dumps(players[1])
    else:
        players[1] = pickle.loads(request.data)
        reply = pickle.dumps(players[0])
    return reply


@blueprint.route('/game/get/<int:player_id>', methods=['GET'])
def get_player(player_id):
    print(player_id)
    if str(player_id) == "1":
        reply = pickle.dumps(players[0])
    else:
        reply = pickle.dumps(players[1])
    return reply


@blueprint.route('/game/join_game', methods=['GET'])
def create_player():
    global currentPlayer
    currentPlayer += 1
    if currentPlayer > 2:
        return "game is full"
    return pickle.dumps(str(currentPlayer))


@blueprint.route('/game/leave', methods=['GET'])
def leave():
    global currentPlayer, players
    currentPlayer -= 1
    players = players_for_online.copy()
