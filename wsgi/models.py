import datetime

from bson import ObjectId


__author__ = 'aguzun'
from passlib.apps import custom_app_context as pwd_context

from core import DB


class User:
    def __init__(self, data):
        self.id = str(data.get("_id"))
        self.email = data.get("email")
        self.password_hash = data.get("password_hash")


    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    @staticmethod
    def get(user_id):
        result = DB.users.find_one({"_id": ObjectId(user_id)})
        if result:
            return User(result)
        else:
            return None

    @staticmethod
    def get_by_email(username):
        result = DB.users.find_one({"email": username})
        if result:
            return User(result)
        else:
            return None

    @staticmethod
    def register(email, password):
        admin = User.get_admin()
        if not admin:
            role = "ADMIN"
        else:
            role = "NORMAL"
        DB.users.insert({
            "email": email,
            "password_hash": User.hash_password(password),
            "registered_on": datetime.datetime.now(),
            "role": role
        })

    @staticmethod
    def get_admin():
        return DB.users.find_one({"role": "ADMIN"})

    def __repr__(self):
        return '<User %r>' % (self.email)
