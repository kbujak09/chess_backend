from flask import Blueprint
from controllers.chess_controller import create_game, save_user, get_open_games, get_game, add_player, change_status, make_move, get_board, get_status

chess_routes = Blueprint('chess_routes', __name__)

chess_routes.route('/games', methods=['POST'])(create_game)

chess_routes.route('/users', methods=['POST'])(save_user)

chess_routes.route('/games', methods=['GET'])(get_open_games)

chess_routes.route('/games/<game_id>', methods=['GET'])(get_game)

chess_routes.route('/games/<game_id>/players', methods=['POST'])(add_player)
  
chess_routes.route('games/<game_id>/status', methods=['POST'])(change_status)
  
chess_routes.route('games/<game_id>/moves', methods=['POST'])(make_move)
  
chess_routes.route('games/<game_id>/moves', methods=['GET'])(get_board)

chess_routes.route('games/<game_id>/status', methods=['GET'])(get_status)