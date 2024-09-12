from flask_socketio import join_room, leave_room, send, emit
from . import socketio

rooms = {}

@socketio.on('join')
def on_join(data):
  user_id = data['id']
  username = data['username']
  room = data['room']
  
  print(user_id, username)
  
  join_room(room)
  
  if room not in rooms:
    rooms[room] = []
  
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