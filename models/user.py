import uuid

from db import db

class User:
  def __init__(self, username, password):
    self._id = uuid.uuid4()
    self.username = username
    self.password = password
    
  def save_to_db(self):
    user_data = {
      "_id": str(self._id),
      "username": self.username,
      "password": self.password
    }
    db.users.insert_one(user_data)
    