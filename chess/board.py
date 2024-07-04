from chess.piece import Pawn, Bishop, Knight, Rook, Queen, King

class Board:
  def __init__(self):
    self.board = [[None for _ in range(8)] for _ in range(8)]
    self.setup_pieces()
    
  def setup_pieces(self):
    for y in range(8):
      self.board[1][y] = Pawn('white')
      self.board[6][y] = Pawn('black')
    
    pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    
    for i, piece in enumerate(pieces):
      self.board[0][i] = piece('white')
      self.board[7][i] = piece('black')
    
  def move_piece(self, start_pos, end_pos):
    piece = self.board[start_pos[0]][start_pos[1]]
    self.board[end_pos[0]][end_pos[1]] = piece
    self.board[start_pos[0]][start_pos[1]] = None
    
  def is_empty(self, pos):
    if self.board[pos[0]][pos[1]] is None: 
      return True
    return False
  
  def get_piece_at(self, pos):
    if self.board[pos[0]][pos[1]] != None:
      return self.board[pos[0]][pos[1]].get_piece_type()
    else:
      return None
  
  def get_king_position(self, color):
    for row in range(8):
      for col in range(8):
        field = self.board[row][col]
        if field is not None and field.get_piece_type() == 'king' and field.get_color() == color:
          return (row, col)
        
  def is_check(self, color):
    king_field = self.get_king_position(color)
    opposite_color = 'black' if color == 'white' else 'white'
    for row in range(8):
      for col in range(8):
        enemy_figure = self.board[row][col]
        if enemy_figure != None and enemy_figure.get_color() == opposite_color:
          if king_field in enemy_figure.moves((row, col), self.board):
            return True       
          else:
            return False 
  
  
  