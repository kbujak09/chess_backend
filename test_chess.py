import pytest

from chess.board import Board

from chess.piece import Pawn, Bishop, Knight, Rook, Queen, King

@pytest.fixture(autouse=True)
def setup():
    empty_board = [[None for _ in range(8)] for _ in range(8)]
    test_board = Board()
    return empty_board, test_board

def test_pawn_init():
    white_pawn = Pawn('white')
    black_pawn = Pawn('black')
    
    assert white_pawn.piece_type == 'pawn'
    assert white_pawn.color == 'white'
    
    assert black_pawn.piece_type == 'pawn'
    assert black_pawn.color == 'black'
  
def test_white_pawn_moves(setup):
    empty_board, _ = setup
    white_pawn = Pawn('white')
    empty_board[3][1] = white_pawn
    assert white_pawn.moves((3, 1), empty_board) == [(4, 1)]
  
def test_black_pawn_moves(setup):
    empty_board, _ = setup
    black_pawn = Pawn('black')
    empty_board[5][0] = black_pawn
    assert black_pawn.moves((5, 0), empty_board) == [(4, 0)]
    
def test_double_pawn_move(setup):
    empty_board, _ = setup
    white_pawn = Pawn('white')
    empty_board[1][0] = white_pawn
    assert white_pawn.moves((1, 0), empty_board) == [(2, 0), (3, 0)]
    
def test_blocked_pawn_moves(setup):
    empty_board, _ = setup
    white_pawn = Pawn('white')
    black_pawn = Pawn('black')
    empty_board[1][0] = white_pawn
    empty_board[2][0] = black_pawn
    assert white_pawn.moves((1, 0), empty_board) == []
    
def test_figures_placement(setup):
    _, test_board = setup
    figures = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(8):
        # tests figures placement
        assert test_board.board[0][i].piece_type == figures[i] and test_board.board[0][i].color == 'white'
        assert test_board.board[7][i].piece_type == figures[i] and test_board.board[7][i].color == 'black'
        # tests pawns placement
        assert test_board.board[1][i].piece_type == 'pawn' and test_board.board[1][i].color == 'white'
        assert test_board.board[6][i].piece_type == 'pawn' and test_board.board[6][i].color == 'black'

def test_bishop_moves(setup):
    empty_board, _ = setup
    bishop = Bishop('white')
    pawn = Pawn('white')
    empty_board[4][5] = bishop
    empty_board[5][4] = pawn
    print(sorted(bishop.moves((4, 5), empty_board))) 
    assert sorted(bishop.moves((4, 5), empty_board)) == sorted([(5, 6), (6, 7), (3, 4), (2, 3), (1, 2), (0, 1), (3, 6), (2, 7)])
    
def test_blocked_bishop_moves(setup):
    empty_board, _ = setup
    bishop = Bishop('black')
    pawn = Pawn('black')
    empty_board[0][0] = bishop
    empty_board[2][2] = pawn
    print(bishop.moves((0, 0), empty_board))
    assert bishop.moves((0, 0), empty_board) == [(1, 1)]
    
def test_knight_moves(setup):
    empty_board, _ = setup
    knight = Knight('white')
    pawn = Pawn('white')
    empty_board[4][5] = knight
    empty_board[5][3] = pawn
    assert sorted(knight.moves((4, 5), empty_board)) == sorted([(6, 4), (2, 4), (3, 3), (6, 6), (5, 7), (3, 7), (2, 6)]) 
    
def test_rook_moves(setup):
    empty_board, _ = setup
    rook = Rook('white')
    black_pawn = Pawn('black')
    white_pawn = Pawn('white')
    empty_board[0][0] = rook
    empty_board[4][0] = white_pawn
    empty_board[0][4] = black_pawn
    assert sorted(rook.moves((0, 0), empty_board)) == sorted([(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 0)])
    
def test_queen_moves(setup):
    empty_board, _ = setup
    queen = Queen('white')
    white_pawn = Pawn('white')
    black_pawn = Pawn('black')
    empty_board[2][3] = queen
    empty_board[3][3] = black_pawn
    empty_board[2][5] = white_pawn
    assert sorted(queen.moves((2,3), empty_board)) == sorted([(5, 0), (4, 1), (3, 2), (2, 0), (2, 1), (2, 2), (0, 3), (1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (2, 4), (3, 3), (1, 4), (0, 5), (0, 1), (1, 2)])

def test_king_moves(setup):
    empty_board, _ = setup
    king = King('white')
    white_pawn = Pawn('white')
    black_pawn = Pawn('black')
    empty_board[3][3] = king
    empty_board[4][3] = white_pawn
    empty_board[3][4] = black_pawn
    assert sorted(king.moves((3,3), empty_board)) == sorted([(4, 2), (4, 4), (3, 2), (3, 4), (2, 2), (2, 3), (2, 4)])
    
def test_moving_piece(setup):
    _, test_board = setup
    test_board.move_piece((1, 0), (2, 0))
    assert test_board.board[1][0] is None
    assert test_board.board[2][0] is not None
    
def test_is_empty(setup):
    _, test_board = setup
    assert test_board.is_empty((3, 0)) == True
    assert test_board.is_empty((1, 0)) == False
    
def test_get_piece_at(setup):
    _, test_board = setup
    assert test_board.get_piece_at((0, 0)) == 'rook'
    assert test_board.get_piece_at((0, 2)) == 'bishop'
    assert test_board.get_piece_at((3, 0)) == None

def test_get_king_position(setup):
    _, test_board = setup
    assert test_board.get_king_position('white') == (0, 4)
    assert test_board.get_king_position('white') != (2, 5)
    assert test_board.get_king_position('black') == (7, 4)
    
def test_is_check(setup):
    _, test_board = setup
    black_rook = Rook('black')
    test_board.board[1][4] = None
    test_board.board[5][4] = black_rook
    assert test_board.is_check('black') == False
    assert test_board.is_check('white') == True
    
def test_get_all_color_moves(setup):
    _, test_board = setup
    assert sorted(test_board.get_all_color_moves('white')) == sorted([(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)])
    
def test_is_checkmate(setup):
    _, test_board = setup
    white_queen = Queen('white')
    black_knight = Knight('black')
    test_board.board[7][3] = None
    test_board.board[7][2] = white_queen
    test_board.board[2][3] = black_knight
    assert test_board.is_checkmate('black') == True
    assert test_board.is_checkmate('white') == False
    
def test_get_king_legal_moves(setup):
    _, test_board = setup
    test_board.board[7][3] = None
    test_board.board[6][3] = None
    test_board.board[1][3] = None
    assert test_board.get_king_legal_moves('white') == [(1, 3)]
    assert test_board.get_king_legal_moves('black') == []
    
def test_is_stalemate(setup):
    _, test_board = setup
    test_board.clear_board()
    white_king = King('white')
    black_king = King('black')
    white_pawn = Pawn('white')
    test_board.board[7][0] = black_king
    test_board.board[5][1] = white_king
    test_board.board[6][0] = white_pawn
    assert test_board.is_stalemate('white') == False
    assert test_board.is_stalemate('black') == True
    