__author__ = 'aguzun'

from flask import json
import requests

from uwsgi_tasks import task, TaskExecutor

from core import app

SLACK_NOTIFY_HOOK_CONFIG = "SLACK_NOTIFY_HOOK_CONFIG"


@task(executor=TaskExecutor.AUTO)
def notify_camera_state_changed(camera):
    # some long running task here
    if SLACK_NOTIFY_HOOK_CONFIG in app.config:
        try:
            if camera.get('active'):
                state_text = "Activated"
            else:
                state_text = "Deactivated"

            payload = {
                'text': "Camera <" + camera.get('name') + "> was " + state_text
            }
            requests.post(app.config.get(SLACK_NOTIFY_HOOK_CONFIG), data=json.dumps(payload))
        except Exception, e:
            app.logger.error("Could not send slack notification", e)
    else:
        app.logger.info("Slack hook not configured. No notification is going to be sent")


@task(executor=TaskExecutor.AUTO)
def notify_new_image(camera, image_url):
    # some long running task here
    if SLACK_NOTIFY_HOOK_CONFIG in app.config:
        try:
            payload = {
                'text': camera.get('name') + " captured new  <" + image_url + "|image>"
            }
            requests.post(app.config.get(SLACK_NOTIFY_HOOK_CONFIG), data=json.dumps(payload))
        except Exception, e:
            app.logger.error("Could not send slack notification", e)
    else:
        app.logger.info("Slack hook not configured. No notification is going to be sent")
