import pytest

from chess.board import Board

from chess.piece import Pawn, Bishop, Knight, Rook, Queen, King

empty_board = [[None for _ in range(8)] for _ in range(8)]

test_board = Board()

def test_pawn_init():
  white_pawn = Pawn('white')
  black_pawn = Pawn('black')
  
  assert white_pawn.piece_type == 'pawn'
  assert white_pawn.color == 'white'
  
  assert black_pawn.piece_type == 'pawn'
  assert black_pawn.color == 'black'
  
def test_white_pawn_moves():
    white_pawn = Pawn('white')
    empty_board[3][1] = white_pawn
    assert white_pawn.moves((3, 1), empty_board) == [(4, 1)]
    
def test_black_pawn_moves():
    black_pawn = Pawn('black')
    empty_board[5][0] = black_pawn
    assert black_pawn.moves((5, 0), empty_board) == [(4, 0)]
    
def test_double_pawn_move():
    white_pawn = Pawn('white')
    empty_board[1][0] = white_pawn
    assert white_pawn.moves((1, 0), empty_board) == [(2,0), (3, 0)]   
    
def test_blocked_pawn_moves():
    white_pawn = Pawn('white')
    black_pawn = Pawn('black')
    empty_board[1][0] = white_pawn
    empty_board[2][0] = black_pawn
    assert white_pawn.moves((1, 0), empty_board) == []
    
def test_figures_placement():
    figures = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(8):
        assert test_board.board[0][i].piece_type == figures[i] and test_board.board[0][i].color == 'white'
        assert test_board.board[1][i].piece_type == 'pawn' and test_board.board[1][i].color == 'white'
        assert test_board.board[7][i].piece_type == figures[i] and test_board.board[7][i].color == 'black'
        assert test_board.board[6][i].piece_type == 'pawn' and test_board.board[6][i].color == 'black'

def test_bishop_moves():
    bishop = Bishop('white')
    empty_board[4][5] = bishop
    assert sorted(bishop.moves((4, 5), empty_board)) == sorted([(5, 4), (6, 3), (7, 2), (5, 6), (6, 7), (3, 4), (2, 3), (1, 2), (0, 1), (3, 6), (2, 7)])
        
    
    