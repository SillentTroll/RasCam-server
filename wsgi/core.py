from flask.ext import restful
from flask import Flask
from flask_jwt import JWT
from gridfs import GridFS
from pymongo import MongoClient
from uwsgi_tasks import set_uwsgi_callbacks

from redis_client import RedisClient

app = Flask(__name__)
app.config.from_pyfile("config/config.py", silent=False)

set_uwsgi_callbacks()

DB = MongoClient(app.config.get('MONGO_URI'))[app.config.get('MONGODB_DB')]
FS = GridFS(DB)
api = restful.Api(app)
jwt = JWT(app)
redis_client = RedisClient(app)
