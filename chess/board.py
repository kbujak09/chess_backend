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
    
  def get_king_position(self, color, isPiece=False):
    for row in range(8):
      for col in range(8):
        field = self.board[row][col]
        if field and field.get_piece_type() == 'king' and field.get_color() == color:
          if isPiece:
            return self.board[row][col]
          else:
            return (row, col)
          
  def is_check(self, color):
    king_field = self.get_king_position(color)
    opposite_color = 'black' if color == 'white' else 'white'
    for row in range(8):
      for col in range(8):
        enemy_figure = self.board[row][col]
        if enemy_figure and enemy_figure.get_color() == opposite_color:
          if king_field in enemy_figure.moves((row, col), self.board):
            return True       
    return False
            
  def get_all_color_moves(self, color):
    moves = []
    for row in range(8):
      for col in range(8):
        piece = self.board[row][col]
        if piece and piece.get_color() == color:
          for move in piece.moves((row, col), self.board):
            if move not in moves:
              moves.append(move)
    return moves
            
  def is_checkmate(self, color):
    enemy_color = 'white' if color == 'black' else 'black'
    # checks if is even a check
    if not self.is_check(color):
      return False
    if self.is_check(color):
      for row in range(8):
        for col in range(8):
          piece = self.board[row][col]
          # checks if king can move
          if piece and piece.get_piece_type() == 'king' and piece.get_color() == color:
            for move in piece.moves((row, col), self.board):
              if move not in self.get_all_color_moves(enemy_color):
                return False
          # checks if attacking piece can be blocked or taken
          if piece and piece.get_color() == color:
            for move in piece.moves((row, col), self.board):
              saved_piece = self.board[move[0]][move[1]]
              self.move_piece((row, col), move)
              if not self.is_check(color):
                self.move_piece(move, (row, col))
                self.board[move[0]][move[1]] = saved_piece
                return False
              else:
                self.move_piece(move, (row, col))
                self.board[move[0]][move[1]] = saved_piece
    return True
    
  def print_board(self):
    piece_symbols = {
        'pawn': {'white': 'P', 'black': 'p'},
        'rook': {'white': 'R', 'black': 'r'},
        'knight': {'white': 'N', 'black': 'n'},
        'bishop': {'white': 'B', 'black': 'b'},
        'queen': {'white': 'Q', 'black': 'q'},
        'king': {'white': 'K', 'black': 'k'}
    }
        
    for row in self.board:
        row_str = ''
        for piece in row:
            if piece is None:
                row_str += '.'
            else:
                piece_type = piece.get_piece_type().lower()
                color = piece.get_color()
                row_str += piece_symbols[piece_type][color]
        print(row_str)

    
  def clear_board(self):
    for row in range(8):
      for col in range(8):
        self.board[row][col] = None
          
  def get_king_legal_moves(self, color):
    king = self.get_king_position(color, True)
    king_position = self.get_king_position(color)
    legal_moves = []
      
    for move in king.moves(self.get_king_position(color), self.board):
      saved_piece = self.board[move[0]][move[1]]
      self.move_piece(king_position, move)
        
      if not self.is_check(color):
        legal_moves.append(move)
          
      self.move_piece(move, king_position)
      self.board[move[0]][move[1]] = saved_piece
      
    return legal_moves
      
    
  def is_stalemate(self, color):
    for row in range(8):
      for col in range(8):
        piece = self.board[row][col]
        if piece and piece.get_color() == color:
          if piece.get_piece_type() == 'king' and self.get_king_legal_moves(color):
            return False
          elif piece.get_piece_type() != 'king' and piece.moves((row, col), self.board):  
            return False 
    return True
    
      
    
    
    