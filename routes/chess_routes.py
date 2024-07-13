from __main__ import app
from flask import jsonify
from chess.game import Game

@app.route('/create_game', methods=['POST'])
def create_game():
  game = Game()
  return jsonify(game.game_board.board_to_json())