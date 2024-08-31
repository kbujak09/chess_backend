from flask_socketio import join_room, leave_room, send
from . import socketio

@socketio.on('join')
def on_join(data):
  user_id = data['id']
  room = data['room']
  join_room(room)
  send(user_id + ' has entered the room.', to=room)
  
@socketio.on('leave')
def on_leave(data):
  user_id = data['id']
  room = data['room']
  leave_room(room)
  send(user_id + ' has left the room.', to=room)