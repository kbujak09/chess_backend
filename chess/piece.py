class Piece:
  def __init__(self, piece_type, color):
    self.piece_type = piece_type
    self.color = color
    
class Pawn(Piece):
  def __init__(self, color):
    super().__init__('pawn', color)
    
  def moves(self, position, board):
    moves = []
    x, y = position
    direction = 1 if self.color == 'white' else -1
    
    if 0 <= x + direction < 8 and board[x + direction][y] is None:
      moves.append((x + direction, y))
      if board[x + 2 * direction][y] is None and ((self.color == 'white' and x == 1) or (self.color == 'black' and x == 6)):
        moves.append((x + 2 * direction, y))
          
    if (0 <= x + direction < 8):
      if (0 <= y - 1) and board[x + direction][y - 1] is not None and board[x + direction][y - 1].color != self.color:
        moves.append((x + direction, y - 1))
      if (8 > y + 1) and board[x + direction][y + 1] is not None and board[x + direction][y + 1].color != self.color:
        moves.append((x + direction, y + 1))
    return moves
  
pass
    
class Bishop(Piece):
  def __init__(self, color):
    super().__init__('bishop', color)
    
  def moves(self, position, board):
    moves = []
    x, y = position
    direction = 1 if self.color == 'white' else -1
    move_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
  
    for d in move_directions:
      row, col = x, y
      while True:
        row += d[0]
        col += d[1]
        if 0 <= row < 8 and 0 <= col < 8 and board[row][col] is None:
          if (row, col) not in moves:
            moves.append((row, col))      
        else:
          break
    print(moves)
    return moves
pass
      
    
class Knight(Piece):
  def __init__(self, color):
    super().__init__('knight', color)
    
class Rook(Piece):
  def __init__(self, color):
    super().__init__('rook', color)
    
class Queen(Piece):
  def __init__(self, color):
    super().__init__('queen', color)
    
class King(Piece):
  def __init__(self, color):
    super().__init__('king', color)