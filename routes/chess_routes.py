from flask import jsonify, Blueprint, request
from chess.game import Game
from models.user import User
from helpers import reinitialize_game

from db import db

chess_routes = Blueprint('chess_routes', __name__)

@chess_routes.route('/game', methods=['POST'])
def create_game():
  data = request.json
  playerId = data['playerId']
  gameId = data['gameId']
  username = data['playerUsername']
  game = Game(playerId, username, gameId)
  game.save_to_db()
  return jsonify(game.game_board.board_to_json())

@chess_routes.route('/save_user', methods=['POST'])
def save_user():
  data = request.json
  user = User(data['username'], data['email'], data['password'])
  db['users'].insert_one(user.to_dict())
  return

@chess_routes.route('/open_games', methods=['GET'])
def get_open_games():
  user_id = request.args.get('userId')
  games = db['games'].find({
    'status': 'open',
    '$nor': [
      {'players.white.id': user_id},
      {'players.black.id': user_id}
    ]
  })
  games_list = list(games)

  return jsonify(games_list)

@chess_routes.route('/game/<id>', methods=['GET'])
def get_game(id):
  game_data = db['games'].find_one({'_id': id })
  
  game = reinitialize_game(game_data)
  
  return jsonify(game.to_json())