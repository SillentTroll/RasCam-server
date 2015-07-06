import pickle

import redis

__author__ = 'aguzun'


class RedisClient:
    def __init__(self, app):
        if ('REDIS_HOST' in app.config) and ('REDIS_PORT' in app.config):
            self.redis_store = redis.StrictRedis(
                host=app.config.get('REDIS_HOST'),
                port=app.config.get('REDIS_PORT'))
            self.app = app
        else:
            self.redis_store = None

    def retrieve_image(self, image_id):
        if self.redis_store:
            try:
                return self.redis_store.get(image_id)
            except Exception, e:
                self.app.logger.error("Could not get the image from redis")
                self.app.logger.log_exception(e)
        else:
            return None

    def cache_image(self, image_id, image_content):
        if self.redis_store:
            try:
                self.redis_store.set(image_id, pickle.dumps(image_content))
            except Exception, e:
                self.app.logger.error("Could not add the image to redis")
                self.app.log_exception(e)

    def delete_image(self, image_id):
        if self.redis_store:
            try:
                self.redis_store.delete(image_id)
            except Exception, e:
                self.app.logger.error("Could not delete the image from redis")
                self.app.log_exception(e)

    def publish(self, stream, oid):
        if self.redis_store:
            try:
                self.redis_store.publish(oid, stream)
            except Exception, e:
                self.app.logger.error("Could send to stream")
                self.app.log_exception(e)

    def get_pubsub(self, stream):
        if self.redis_store:
            pubsub = self.redis_store.pubsub()
            pubsub.subscribe(stream)
            return pubsub
        else:
            return None
