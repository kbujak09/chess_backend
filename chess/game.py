from chess.board import Board
import uuid

class Game:
  def __init__(self):
    self.id = str(uuid.uuid4())
    self.game_board = Board()
    self.players = {'white': None, 'black': None}
    self.current_turn = 'white'
    self.game_over = False
  
  def take_turn(self, start_pos, end_pos):
    
    if self.game_board.board[start_pos[0]][start_pos[1]].get_color() != self.current_turn:
      return False
    
    if not self.game_board.make_move(start_pos, end_pos):
      return False
    
    self.current_turn = 'black' if self.current_turn == 'white' else 'black'
    
    if self.game_board.is_checkmate(self.current_turn):
      self.game_over = True
      print(f"{self.current_turn} lost")
    elif self.game_board.is_stalemate(self.current_turn):
      self.game_over = True
      print("stalemate")
      
    return True
  
  def print_board(self):
    return self.game_board.print_board()
  