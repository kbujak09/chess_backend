from flask import Flask, jsonify
from flask_cors import CORS

from chess.game import Game

app = Flask(__name__)
CORS(app)

from routes import chess_routes

if __name__ == '__main__':
  app.run(debug=True)