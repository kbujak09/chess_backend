from chess.game import Game
from chess.piece import Pawn, Rook, Knight, Bishop, Queen, King

def validate_register(username, password, confirm_password):
  if len(username) < 4:
    return 'Username must be at least 4 characters'
  if len(username) > 16:
    return "Username can't be longer than 16 characters"
  if len(password) <= 6:
    return "Password must be at least 6 characters"
  if password != confirm_password:
    return "Passwords doesn't match"
  return True  

def reinitialize_game(game_data):
    # Initialize a new game
    game = Game(
        playerId=None,
        username=None,
        gameId=game_data['_id'],
        initialTime=game_data['initial_time'],
        increment=game_data['increment']
    )

    # Set player information and game state from the database
    game.players = game_data['players']
    game.current_turn = game_data['current_turn']
    game.status = game_data['status']
    game.last_move_time = game_data['last_move_time']
    
    game.game_board.clear_board()
    
    # Set up the board from the saved positions
    for piece_data in game_data['board']['positions']:
        piece_type = piece_data['type']
        color = piece_data['color']
        position = piece_data['position']
        
        # Create the piece and place it on the board
        if piece_type == 'pawn':
            game.game_board.board[position[0]][position[1]] = Pawn(color)
        elif piece_type == 'rook':
            game.game_board.board[position[0]][position[1]] = Rook(color)
        elif piece_type == 'knight':
            game.game_board.board[position[0]][position[1]] = Knight(color)
        elif piece_type == 'bishop':
            game.game_board.board[position[0]][position[1]] = Bishop(color)
        elif piece_type == 'queen':
            game.game_board.board[position[0]][position[1]] = Queen(color)
        elif piece_type == 'king':
            game.game_board.board[position[0]][position[1]] = King(color)
    
    # Restore the move history
    game.game_board.move_history = game_data['board']['history']

    return game