import pickle

from bson import ObjectId
from flask import (make_response, jsonify, render_template)
from gridfs import NoFile
from werkzeug.exceptions import abort

from core import app, api, FS, jwt, redis_store
from models import User


@app.route('/')
@app.route('/cameras')
@app.route('/images')
@app.route('/users/login')
@app.route('/users/configure')
def index():
    return render_template("index.html")


@app.route('/users/configured')
def is_configured():
    # if has admin user, then the server is configured
    if User.get_admin():
        return jsonify(result="OK")
    else:
        return jsonify(result="NOK")


@app.route('/files/<oid>')
def serve_gridfs_file(oid):
    try:
        cached_response = redis_store.get(oid)
        if cached_response:
            return pickle.loads(cached_response)
        else:
            image_file = FS.get(ObjectId(oid))
            response = make_response(image_file.read())
            response.mimetype = image_file.content_type
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Cache-Control'] = 'particular, max-age=31104000'
            redis_store.set(oid, pickle.dumps(response))
            return response
    except NoFile:
        abort(404)


@app.errorhandler(400)
def bad_request_handler(error):
    return make_response(jsonify(
        {'error': error.description if error.description else 'Bad Request'}
    ), 400)


@app.errorhandler(401)
def unauthorised_handler(error):
    return make_response(jsonify(
        {'error': error.description if error.description else 'Unauthorized'}
    ), 401)


@app.errorhandler(405)
def common_handler(error):
    return make_response(jsonify(
        {'error': error.description}
    ), 405)


@jwt.authentication_handler
def verify_password(username, password):
    print "verify password of " + username
    # try to authenticate with username/password
    user = User.get_by_email(username)
    if not user or not user.verify_password(password):
        return None
    else:
        return user


@jwt.user_handler
def load_user(payload):
    return User.get(payload['user_id'])


def register_apis(api):
    from camera_api import CameraStateController, UploadImage, CameraController, CamerasController

    api.add_resource(CameraStateController, '/api/v1/cam/state', '/api/v1/cam/<string:camera_id>/state')
    api.add_resource(UploadImage, '/api/v1/cam/upload')
    api.add_resource(CameraController, '/api/v1/cam/<string:camera_id>')
    api.add_resource(CamerasController, '/api/v1/cam')

    from images_api import ImagesController, ImageController

    api.add_resource(ImagesController, '/api/v1/images')
    api.add_resource(ImageController, '/api/v1/image/<string:image_id>')

    from users_api import UserRegisterController

    api.add_resource(UserRegisterController, "/api/v1/users/register")


register_apis(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
