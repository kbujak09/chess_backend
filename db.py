from flask_pymongo import PyMongo

mongo = None
db = None

def init_db(app):
    global mongo, db
    mongo = PyMongo(app).cx["chess_app"]
    db = mongo.db