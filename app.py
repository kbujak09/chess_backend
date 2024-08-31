from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from websocket import socketio
from websocket.socketio import *
import os

load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = os.getenv('SECRET_KEY')

CORS(app)

db_key = os.getenv("MONGODB_URL")
app.config["MONGO_URI"] = db_key

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
jwt = JWTManager(app)

from db import init_db

init_db(app)

socketio.init_app(app)
  
from routes.chess_routes import chess_routes
app.register_blueprint(chess_routes, url_prefix='/api')

from routes.auth_routes import auth_routes
app.register_blueprint(auth_routes, url_prefix='/api')

if __name__ == '__main__':
  socketio.run(app, debug=True)