from flask import Flask, jsonify
from flask_cors import CORS

from chess.board import Board

app = Flask(__name__)
CORS(app)

test_board = Board()

@app.route('/')
def hello_world():
  return jsonify('Hello World!')

if __name__ == '__main__':
  app.run(port=3000)