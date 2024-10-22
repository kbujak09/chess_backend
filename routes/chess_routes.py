from flask import jsonify, Blueprint, request
from chess.game import Game
from models.user import User
from helpers import reinitialize_game

from db import db

chess_routes = Blueprint('chess_routes', __name__)

@chess_routes.route('/games', methods=['POST'])
def create_game():
  data = request.json
  playerId = data['playerId']
  gameId = data['gameId']
  username = data['playerUsername']
  initialTime = data['initialTime']
  increment = data['increment']
  game = Game(playerId, username, gameId, initialTime, increment)
  game.save_to_db()
  return jsonify(game.game_board.board_to_json())

@chess_routes.route('/users', methods=['POST'])
def save_user():
  data = request.json
  user = User(data['username'], data['email'], data['password'])
  db['users'].insert_one(user.to_dict())
  return

@chess_routes.route('/games', methods=['GET'])
def get_open_games():
  status = request.args.get('status')
  user_id = request.args.get('userId')
  
  if status == 'open':
    games = db['games'].find({
      'status': 'open',
      '$nor': [
        {'players.white.id': user_id},
        {'players.black.id': user_id}
      ]
    })
    games_list = list(games)

  return jsonify(games_list)

@chess_routes.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):
  game_data = db['games'].find_one({'_id': game_id })
  
  game = reinitialize_game(game_data)
  
  return jsonify(game.to_json())

@chess_routes.route('/games/<game_id>/players', methods=['POST'])
def add_player(game_id):
    player_data = request.get_json()
    
    player = player_data.get('player')

    game_data = db['games'].find_one({'_id': game_id})
    
    players = game_data.get('players')
    
    if players['white']['id'] == player.get('id') or players['black']['id'] == player.get('id'):
      return jsonify({'message': 'Player is already saved'})
    
    if players['white']['id'] is None:
      players['white']['id'] = player.get('id')
      players['white']['username'] = player.get('username')
    elif players['black']['id'] is None:
      players['black']['id'] = player.get('id')
      players['black']['username'] = player.get('username')
    
    db['games'].update_one({'_id': game_id}, {'$set': {'players': players}})
    
    return jsonify({'message': 'Player added successfully!'})
  
@chess_routes.route('games/<game_id>/status', methods=['POST'])
def change_status(game_id):
  status = request.get_json()
  
  db['games'].update_one({'_id': game_id}, {'$set': {'status': status['status']}})
  
  return jsonify({'message': 'Game status changed.'})
  
@chess_routes.route('games/<game_id>/moves', methods=['POST'])
def make_move(game_id):
  data = request.get_json()['moveData']
  
  game_data = db['games'].find_one({'_id': game_id})
  
  game = reinitialize_game(game_data)
  
  game.take_turn(tuple(data['start']), tuple(data['end']))
  
  game.game_board.print_board()
  
  game.update_game_data()
  
  return jsonify()
  