class Piece:
  def __init__(self, piece_type, color):
    self.piece_type = piece_type
    self.color = color
    
  def get_piece_type(self):
    return self.piece_type
    
  def get_color(self):
    return self.color
pass
    
class LineMoverPiece(Piece):
  def moves_in_directions(self, position, board, move_directions):
    moves = []
    x, y = position
  
    for d in move_directions:
      row, col = x, y
      while True:
        row += d[0]
        col += d[1]
        if 0 <= row < 8 and 0 <= col < 8:
          if board[row][col] is None:
            moves.append((row, col))
          elif board[row][col].color != self.color:
            moves.append((row, col))
            break 
          else:
            break     
        else:
          break
    return moves
pass

class Pawn(Piece):
  def __init__(self, color):
    super().__init__('pawn', color)
    
  def moves(self, position, board):
    moves = []
    x, y = position
    direction = 1 if self.color == 'white' else -1
    
    if 0 <= x + direction < 8 and board[x + direction][y] is None:
      moves.append((x + direction, y))
      if 0 <= x + direction*2 < 8 and board[x + 2 * direction][y] is None and ((self.color == 'white' and x == 1) or (self.color == 'black' and x == 6)):
        moves.append((x + 2 * direction, y))
          
    if (0 <= x + direction < 8):
      if (0 <= y - 1) and board[x + direction][y - 1] is not None and board[x + direction][y - 1].color != self.color:
        moves.append((x + direction, y - 1))
      if (8 > y + 1) and board[x + direction][y + 1] is not None and board[x + direction][y + 1].color != self.color:
        moves.append((x + direction, y + 1))
    return moves
pass
    
class Bishop(LineMoverPiece):
  def __init__(self, color):
    super().__init__('bishop', color)
    
  def moves(self, position, board):
    move_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    return self.moves_in_directions(position, board, move_directions)
pass
      
class Knight(Piece):
  def __init__(self, color):
    super().__init__('knight', color)
  
  def moves(self, position, board):
    moves = []
    x, y = position
    move_direction = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2)]
    
    for d in move_direction:
      temp_x = x + d[0]
      temp_y = y + d[1]
      if 0 <= temp_x < 8 and 0 <= temp_y < 8:
        if board[temp_x][temp_y]is None:
          moves.append((temp_x, temp_y))
        elif board[temp_x][temp_y]is not None and board[temp_x][temp_y].color != self.color:
          moves.append((temp_x, temp_y))
    return moves
pass
    
class Rook(LineMoverPiece):
  def __init__(self, color):
    super().__init__('rook', color)
    
  def moves(self, position, board):
    move_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return self.moves_in_directions(position, board, move_directions)
pass
    
class Queen(LineMoverPiece):
  def __init__(self, color):
    super().__init__('queen', color)
  
  def moves(self, position, board):
    move_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    return self.moves_in_directions(position, board, move_directions)
pass

class King(Piece):
  def __init__(self, color):
    super().__init__('king', color)
    
  def moves(self, position, board):
    moves = []
    x, y = position
    move_directions = [(1, -1), (1, 0), (1, 1),
                       (0, -1), (0, 1),
                       (-1, -1), (-1, 0), (-1, 1)]
    
    for d in move_directions:
      row = x + d[0]
      col = y + d[1]
      if 0 <= row < 8 and 0 <= col < 8:
        if board[row][col] is None or board[row][col].color != self.color:
          moves.append((row, col))
    return moves
pass