from flask import jsonify, request
from chess.game import Game
from models.user import User
from helpers import reinitialize_game, update_timers

from db import db

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

def save_user():
  data = request.json
  user = User(data['username'], data['email'], data['password'])
  db['users'].insert_one(user.to_dict())
  return

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

def get_game(game_id):
  game_data = db['games'].find_one({'_id': game_id })
  
  game = reinitialize_game(game_data)
  
  update_timers(game)
  
  return jsonify(game.to_json())

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
  
def change_status(game_id):
  game_data = db['games'].find_one({'_id': game_id})

  game = reinitialize_game(game_data)

  status = request.get_json()

  if game.status == 'open' and status['status'] == 'live':
    game.start_game()
    game.update_game_data()
    return jsonify({'message': 'Game started'})
  
  db['games'].update_one({'_id': game_id}, {'$set': {'status': status['status']}})
  
  return jsonify({'message': 'Game status changed.'})

def make_move(game_id):
  data = request.get_json()['moveData']
  
  game_data = db['games'].find_one({'_id': game_id})
  
  game = reinitialize_game(game_data)
  
  move = game.take_turn(tuple(data['start']), tuple(data['end']))
  
  if not move['status']:
    return jsonify({'status': False, 'message': move['message'], 'gameStatus': move['gameStatus'], 'players': game.players})
  
  game.update_game_data()
  
  return jsonify({'status': True, 'board': game.game_board.board_to_json(), 'type': move['type'], 'gameStatus': move['gameStatus'], 'players': game.players})

def get_board(game_id):
  game_data = db['games'].find_one({'_id': game_id})
  
  game = reinitialize_game(game_data)
  
  if not game.game_board:
    return jsonify({'status': False, 'message': 'Game board not found'})
  
  return jsonify({'status': True, 'board': game.game_board.board_to_json()})

def get_status(game_id):
  game_data = db['games'].find_one({'_id': game_id})

  game = reinitialize_game(game_data)

  update_timers(game)

  if game.players['white']['time'] <= 0:
    game.status = 'black won' 
  elif game.players['black']['time'] <= 0:
    game.status = 'white won'

  game.update_game_data()

  return jsonify({'status': game.status})