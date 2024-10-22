from chess.board import Board
import uuid
import random
from datetime import datetime

from db import db

class Game:
  def __init__(self, playerId, username, gameId, initialTime, increment):
    self.id = gameId
    self.game_board = Board()
    if random.choice([True, False]):
      self.players = {
        'white': {'username': username, 'id': playerId, 'time': initialTime},
        'black': {'username': None, 'id': None, 'time': initialTime}
      }
    else:
      self.players = {
        'black': {'username': username, 'id': playerId,  'time': initialTime},
        'white': {'username': None, 'id': None,  'time': initialTime}
      }
    self.moves = []
    self.current_turn = 'white'
    self.status = 'open'
    self.initial_time = initialTime
    self.increment = increment
  
  def take_turn(self, start_pos, end_pos):
    
    if self.game_board.board[start_pos[0]][start_pos[1]].get_color() != self.current_turn:
      return False
    
    if not self.game_board.make_move(start_pos, end_pos):
      return False
    
    self.current_turn = 'black' if self.current_turn == 'white' else 'black'
    
    if self.game_board.is_checkmate(self.current_turn):
      self.status = 'ended'
      print(f"{self.current_turn} lost")
    elif self.game_board.is_stalemate(self.current_turn):
      self.status = 'ended'
      print("stalemate")
      
    return True
  
  def print_board(self):
    return self.game_board.print_board()

  def save_to_db(self):
    game_data = {
      "_id": str(self.id),
      "players": self.players,
      "current_turn": self.current_turn,
      "status": self.status,
      "board": {
        "positions": self.game_board.board_to_json(),
        "history": self.game_board.move_history
      },
      "moves": self.moves,
      "initial_time": self.initial_time,
      "increment": self.increment
    }
    db.games.insert_one(game_data)
  
  def to_json(self):
    
    created_at = datetime.now()
    
    game_data = {
      "_id": str(self.id),
      "players": self.players,
      "current_turn": self.current_turn,
      "status": self.status,
      "board": {
        "positions": self.game_board.board_to_json(),
        "history": self.game_board.move_history
      },
      "moves": self.moves,
      "initial_time": self.initial_time,
      "created_at": created_at
    }
    return game_data
  
  def update_game_data(self):
    game_data = {
      "_id": str(self.id),
      "players": self.players,
      "current_turn": self.current_turn,
      "status": self.status,
      "board": {
        "positions": self.game_board.board_to_json(),
        "history": self.game_board.move_history
      },
      "moves": self.moves,
      "initial_time": self.initial_time,
      "increment": self.increment
    }
    
    db.games.update_one({'_id': self.id}, {'$set': game_data})
    
    return game_data