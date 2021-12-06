from flask import Flask
from flask_restx import Api
from flask_pymongo import PyMongo

LOGIN = 'stypa98'
PASSWORD = 'Qwerty228'

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = f"mongodb+srv://{LOGIN}:{PASSWORD}@cluster0.9xtzt.mongodb.net/database_name?retryWrites" \
                          f"=true&w=majority "
mongo = PyMongo(app)
db = mongo.db.collection_name
