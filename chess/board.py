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