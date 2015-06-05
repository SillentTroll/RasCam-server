from datetime import timedelta
import os


PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.urandom(24)
API_PREFIX = "/api/v1/"

# webcam images upload
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

# Mongo
MONGO_DB_USER = ""
MONGO_DB_PASS = ""
MONGODB_DB = "home_center"
MONGODB_HOST = "db"
MONGODB_PORT = 27017
MONGO_URI = "mongodb://{0}:{1}/{2}".format(MONGODB_HOST, MONGODB_PORT, MONGODB_DB)

# Redis
REDIS_HOST = "redis"
REDIS_PORT = 6379

# SECURITY
JWT_AUTH_URL_RULE = API_PREFIX + 'users/auth'
JWT_EXPIRATION_DELTA = timedelta(minutes=60)