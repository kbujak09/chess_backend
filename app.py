from flask import Flask, jsonify
from flask_cors import CORS

from chess.board import Board

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
  return jsonify('Hello World!')

@app.route('/get_board')
def get_board():
  test_board = Board()
  board_data = {
    'board': [[str(f"{test_board.board[i][j].color}_{test_board.board[i][j].piece_type}") if test_board.board[i][j] else None for j in range(8)] for i in range(8)]
  }
  return jsonify(board_data)

if __name__ == '__main__':
  app.run(debug=True)