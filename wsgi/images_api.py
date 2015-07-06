import datetime

from bson import ObjectId
from flask import url_for, jsonify
from flask.ext import restful
from flask_jwt import jwt_required, current_user
import pymongo

from core import app, DB, FS, redis_client


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

    @staticmethod
    @jwt_required()
    def delete(day):
        date_to_remove_min = datetime.datetime.strptime(day, "%Y-%m-%d")
        date_to_remove_max = date_to_remove_min + datetime.timedelta(1)

        images_to_delete = DB.images.find(
            {"$and": [{"date_saved": {"$gte": date_to_remove_min}},
                      {"date_saved": {"$lte": date_to_remove_max}}]})
        images_to_delete_count = images_to_delete.count()
        app.logger.warn("Going to remove %s images from  %s to %s",
                        images_to_delete_count,
                        date_to_remove_min,
                        date_to_remove_max)

        for image_to_delete in images_to_delete:
            ImageController.delete(str(image_to_delete.get("_id")))

        if images_to_delete_count > 0:
            DB.images.history.insert({
                'action': 'delete_all_images',
                'day': date_to_remove_min,
                'count': images_to_delete_count,
                'when': datetime.datetime.now(),
                'user': current_user.email
            })
        return {"result": "OK"}


class ImageController(restful.Resource):
    @staticmethod
    @jwt_required()
    def delete(image_id):
        image = DB.images.find_one({"_id": ObjectId(image_id)})
        if image:
            FS.delete(ObjectId(image.get("image_id")))
            redis_client.delete_image(image.get("image_id"))
            DB.images.remove(image)

        return {"result": "OK"}
