from flask import jsonify, Blueprint, request
from chess.game import Game
from models.user import User

from db import db

chess_routes = Blueprint('chess_routes', __name__)

@chess_routes.route('/create_game', methods=['POST'])
def create_game():
  game = Game()
  game.save_to_db()
  return jsonify(game.game_board.board_to_json())

@chess_routes.route('/save_user', methods=['POST'])
def save_user():
  data = request.json
  user = User(data['username'], data['email'], data['password'])
  db['users'].insert_one(user.to_dict())
  return