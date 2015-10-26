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


# SECURITY
JWT_AUTH_URL_RULE = API_PREFIX + 'users/auth'
JWT_EXPIRATION_DELTA = timedelta(minutes=60)

# Slack config
SLACK_NOTIFY_HOOK_CONFIG = "https://hooks.slack.com/services/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"
SLACK_TEAM_ID = "T0562HCT2"
SLACK_START_COMMAND_TOKEN = "526LAYdxqLctuDlV4FWYta31"
SLACK_STOP_COMMAND_TOKEN = "cFA6Nd3YEsm5uzWCYwjzl2wG"
