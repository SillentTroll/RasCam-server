import datetime

from bson import ObjectId
from flask import url_for, jsonify
from flask.ext import restful
from flask_jwt import jwt_required, current_user
import pymongo

from core import DB, FS, redis_store


class ImagesController(restful.Resource):
    @jwt_required()
    def get(self):
        images = DB.images.find().sort("date_saved", pymongo.DESCENDING)
        results = []
        if images:
            for image_file in images:
                date_time_saved = image_file.get("date_saved")
                image_data = {
                    "id": str(image_file.get("_id")),
                    "camera": image_file.get("camera"),
                    "image_id": str(image_file.get("image_id")),
                    "url": url_for('serve_gridfs_file', oid=str(image_file.get("image_id"))),
                    "time_saved": date_time_saved.time().isoformat(),
                    "date_saved": date_time_saved.date().isoformat()
                }
                if 'date_taken' in image_file:
                    image_file["date_taken"] = str(image_file.get("date_taken")),

                results.append(image_data)

        return jsonify(images=results)


class ImageController(restful.Resource):
    @staticmethod
    @jwt_required()
    def delete(image_id):
        image = DB.images.find_one({"_id": ObjectId(image_id)})
        if image:
            FS.delete(ObjectId(image.get("image_id")))
            redis_store.delete(image.get("image_id"))
            DB.images.remove(image)
            DB.images.history.insert({
                'action': 'remove',
                'image_id': image_id,
                'when': datetime.datetime.now(),
                'user': current_user.email
            })
        return {"result": "OK"}
