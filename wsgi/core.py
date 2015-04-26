from flask import Flask
from flask.ext import restful

from flask_jwt import JWT
from gridfs import GridFS
from pymongo import MongoClient
import redis


app = Flask(__name__)

app.config.from_pyfile("config/config.py", silent=False)
DB = MongoClient(app.config.get('MONGO_URI'))[app.config.get('MONGODB_DB')]
FS = GridFS(DB)
api = restful.Api(app)
jwt = JWT(app)
redis_store = redis.StrictRedis(host=app.config.get('REDIS_HOST'), port=app.config.get('REDIS_PORT'))