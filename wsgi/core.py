from flask import Flask
from flask.ext import restful

from flask_jwt import JWT
import redis


app = Flask(__name__)

app.config.from_pyfile("config/application.cfg", silent=False)
FS = app.config.get('GRID_FS')
DB = app.config.get('MONGO_CLIENT')
api = restful.Api(app)
jwt = JWT(app)
redis_store = redis.StrictRedis(host=app.config.get('REDIS_HOST'), port= app.config.get('REDIS_PORT'))