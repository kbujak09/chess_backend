from flask_socketio import join_room, leave_room, send, emit
from . import socketio

@socketio.on('join')
def on_join(data):
  user_id = data['id']
  username = data['username']
  room = data['room']
    
  join_room(room)
  
  send(user_id + ' has entered the room.', to=room)
  
  new_user = {
    'id': user_id,
    'username': username
  }
  
  emit('playerJoined', new_user, to=room)
  
@socketio.on('leave')
def on_leave(data):
  user_id = data['id']
  room = data['room']
  leave_room(room)
  send(user_id + ' has left the room.', to=room)
  
@socketio.on('move')
def on_move(data):
  pos = data['position']
  userId = data['userId']
  room = data['room']
  moveType = data['type']
  gameStatus = data['gameStatus']
  board = data['board']
  players = data['players']
  emit('enemyMoved', {'pos': pos, 'userId': userId, 'type': moveType, 'gameStatus': gameStatus, 'board': board, 'players': players}, to=room)