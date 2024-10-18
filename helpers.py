from chess.game import Game

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
  game = Game(
    playerId=None,
    username=None,
    gameId=game_data['_id'],
    initialTime=game_data['initial_time'],
    increment=game_data['increment'])

  game.players = game_data['players']
  game.current_turn = game_data['current_turn']
  game.status = game_data['status']

  game.game_board.board_to_json()

  return game