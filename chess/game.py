from chess.board import Board
import random
from datetime import datetime
import time

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
    self.current_turn = 'white'
    self.status = 'open'
    self.initial_time = initialTime
    self.increment = increment
    self.last_move_time = time.time()
  
  def take_turn(self, start_pos, end_pos):
    current_player = self.players[self.current_turn]
    
    print(self.last_move_time, time.time())
    elapsed_time = round(time.time() - self.last_move_time)
    current_player['time'] -= elapsed_time
    self.last_move_time = time.time()
    
    if current_player['time'] <= 0:
      self.status = f"{self.current_turn} lost on time"
      return {'status': False, 'message': 'Time over', 'gameStatus': self.status}
    
    if self.game_board.board[start_pos[0]][start_pos[1]].get_color() != self.current_turn:
      return False
    
    move = self.game_board.make_move(start_pos, end_pos)
    
    if not move['status']:
      return {'status': move['status'], 'message': move['message'], 'gameStatus': self.status}
    
    current_player['time'] += self.increment
    
    self.current_turn = 'black' if self.current_turn == 'white' else 'white'
    
    if self.game_board.is_checkmate(self.current_turn):
      self.status = 'white won' if self.current_turn == 'black' else 'black won'
    elif self.game_board.is_stalemate(self.current_turn):
      self.status = 'stalemate'
      
    return {'status': move['status'], 'type': move['type'], 'gameStatus': self.status}
  
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
      "initial_time": self.initial_time,
      "increment": self.increment,
      "last_move_time": self.last_move_time
    }
    db.games.insert_one(game_data)
  
  def to_json(self):
    
    created_at = datetime.now()
    
    game_data = {
      "_id": str(self.id),
      "players": self.players,
      "current_turn": self.current_turn,
      "status": self.status,
      "increment": self.increment,
      "board": {
        "positions": self.game_board.board_to_json(),
        "history": self.game_board.move_history
      },
      "initial_time": self.initial_time,
      "last_move_time": self.last_move_time,
      "created_at": created_at,
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
      "initial_time": self.initial_time,
      "increment": self.increment,
      "last_move_time": self.last_move_time,
    }
    
    db.games.update_one({'_id': self.id}, {'$set': game_data})
    
    return game_data