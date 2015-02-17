from flask.ext import restful
from flask_restful import reqparse

from models import User


class UserRegisterController(restful.Resource):
    def __init__(self):
        self.register_parser = reqparse.RequestParser()
        self.register_parser.add_argument("email", type=str, required=True, help="Email is required")
        self.register_parser.add_argument("password", type=str, required=True, help="Password is required")
        self.register_parser.add_argument("password_confirm", type=str, required=True,
                                          help="Password confirmation is required")

    def put(self):
        args = self.register_parser.parse_args()
        user = User.get_by_email(args['email'])
        if user:
            return {"result": "NOK", "message": "There is already a user with this username"}, 400
        else:
            if args['password'] == args['password_confirm']:
                User.register(email=args['email'], password=args['password'])
                if User.get_by_email(args['email']):
                    return {"result": "OK"}, 201
                else:
                    return {"result": "NOK"}, 500
            else:
                return {"result": "NOK", "message": "Passwords do not match"}, 400

