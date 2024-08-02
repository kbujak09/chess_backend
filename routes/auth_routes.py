from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.user import User
from helpers import validate_register
from flask_bcrypt import Bcrypt

from db import db

import os

auth_routes = Blueprint('auth_routes', __name__)
bcrypt = Bcrypt()

@auth_routes.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  confirm_password = data.get('confirm_password')
  
  existing_user = db['users'].find({'username': username})
  
  if existing_user:
    return jsonify({'message': 'User with that name already exists'})
  
  validation_result = validate_register(username=username, password=password, confirm_password=confirm_password)
  if validation_result is not True:
    return jsonify({"message": validation_result}), 400 
  
  hashed_password = bcrypt.generate_password_hash(password, 10)
  
  new_user = User(username, hashed_password)
  new_user.save_to_db()
  
  return jsonify({"message": "Registration successful!"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  
  