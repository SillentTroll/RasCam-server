from functools import wraps
import hashlib
import datetime
import mimetypes
import random

from bson import ObjectId
from flask import jsonify
from flask_jwt import jwt_required, current_user
from flask_restful import reqparse
import pymongo
import werkzeug
from werkzeug.utils import secure_filename
from flask.ext import restful

from core import app, FS, DB


api_request_parser = reqparse.RequestParser()
api_request_parser.add_argument('api_key', type=str, required=True, help="Missing api key")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')


def get_cam_by_id(camera_id):
    return DB.cams.find_one({"_id": ObjectId(camera_id)})


def requires_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_args = api_request_parser.parse_args()
        input_api_key = api_args['api_key']

        if not input_api_key:
            restful.abort(401)
        else:
            valid_cam = DB.cams.find_one({"api_key": input_api_key})
            if not valid_cam:
                restful.abort(401, description="Valid api key is required")
            else:
                valid_cam['last_access'] = datetime.datetime.now()
                DB.cams.save(valid_cam)
                return f(*args, **kwargs)

    return decorated_function


class CameraStateController(restful.Resource):
    @requires_api_key
    def get(self):
        args = api_request_parser.parse_args()
        valid_cam = DB.cams.find_one({"api_key": args['api_key']})
        if valid_cam:
            return {'result': 'OK', 'state': valid_cam.get('active')}
        return {'result': 'NOK'}, 401


    @staticmethod
    @jwt_required()
    def post(camera_id):
        if camera_id:
            camera = get_cam_by_id(camera_id)
            if camera:
                camera['active'] = not camera.get('active')
                DB.cams.save(camera)
                DB.cams.history.insert({
                    'action': 'change_state',
                    'camera': camera.get('name'),
                    'when': datetime.datetime.now(),
                    'new_state': camera.get('active'),
                    'user': current_user.email
                })
                return jsonify(result="OK", new_state=camera.get('active'), id=camera_id)
            else:
                return jsonify(result="NOK", error="Invalid camera id")

        return jsonify(result="NOK")


file_upload_parser = api_request_parser.copy()
file_upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files',
                                required=True)
file_upload_parser.add_argument('date', type=str)
file_upload_parser.add_argument('event', type=str)


class UploadImage(restful.Resource):
    @staticmethod
    @requires_api_key
    def post():
        args = file_upload_parser.parse_args()
        request_cam = DB.cams.find_one({"api_key": args['api_key']})
        in_image_file = args['file']
        if in_image_file and allowed_file(in_image_file.filename):
            filename = secure_filename(in_image_file.filename)
            content_type = in_image_file.content_type \
                if in_image_file.content_type else mimetypes.guess_type(in_image_file.filename)[0]

            oid = FS.put(in_image_file, content_type=content_type,
                         filename=filename)
            DB.images.save({
                "image_id": str(oid),
                "date_saved": datetime.datetime.now(),
                "date_taken": args.get('date') if 'date' in args else datetime.datetime.now(),
                "camera": request_cam.get('name'),
                "event": args.get('event')
            })
            return jsonify(status="OK", oid=str(oid))
        return jsonify(status="NOK", error="not allowed file")


class CameraController(restful.Resource):
    @staticmethod
    @jwt_required()
    def delete(camera_id):
        if camera_id:
            cam_by_id = get_cam_by_id(camera_id)
            if cam_by_id:
                DB.cams.remove({"_id": ObjectId(camera_id)})
                DB.cams.history.insert({
                    'action': 'remove',
                    'camera': cam_by_id.get('name'),
                    'when': datetime.datetime.now(),
                    'user': current_user.email
                })

            return jsonify(result="OK")
        return jsonify(result="NOK")


class CamerasController(restful.Resource):
    def __init__(self):
        self.register_parser = reqparse.RequestParser()
        self.register_parser.add_argument('cam_name', type=str, required=True, help='Provide camera name')

    @staticmethod
    @jwt_required()
    def get():
        cameras = []
        for camera in DB.cams.find():
            cameras.append({
                "id": str(camera.get("_id")),
                "name": camera.get('name'),
                "api_key": camera.get('api_key'),
                "active": camera.get('active'),
                "last_access": camera.get('last_access'),
                "registered": camera.get('registered'),
                "ip": camera.get('ip'),
            })
        for camera in cameras:
            # get the last history entry of the camera
            last_events = DB.cams.history.find({"camera": camera.get('name')}) \
                .sort("when", pymongo.DESCENDING) \
                .limit(5)
            if last_events:
                camera['last_events'] = list()
                for last_event in last_events:
                    camera['last_events'].append({
                        "when": last_event.get("when"),
                        "user": last_event.get("user"),
                        "action": last_event.get("action"),
                        "new_state": last_event.get("new_state")
                    })
            last_image = DB.images.find_one({"camera": camera.get('name')}, sort=[("date_saved", pymongo.DESCENDING)])
            if last_image:
                camera["last_image_date"] = last_image.get("date_saved")
        return jsonify(result="OK", cameras=cameras)

    @jwt_required()
    def put(self):
        args = self.register_parser.parse_args()
        input_cam_name = args.get('cam_name')

        existing = DB.cams.find_one({"name": input_cam_name})
        if existing:
            return {'error': "There is already a camera with this name"}, 400
        else:
            new_cam_api_key = hashlib.sha224(str(random.getrandbits(256))).hexdigest()
            DB.cams.insert({
                "name": input_cam_name,
                "api_key": new_cam_api_key,
                "registered": datetime.datetime.now(),
                "active": True
            })
            return {'status': "OK", 'api_key': new_cam_api_key}

