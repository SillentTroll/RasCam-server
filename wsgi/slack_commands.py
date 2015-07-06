from flask_slack import Slack

from camera_api import CameraStateController
from core import DB


class SlackCommands:
    def __init__(self, app):
        self.app = app

        if 'SLACK_TEAM_ID' in app.config:
            slack = Slack(app)
            app.add_url_rule(app.config.get('API_PREFIX') + 'slack', view_func=slack.dispatch)

            if 'SLACK_START_COMMAND_TOKEN' in app.config:
                @slack.command('start', token=app.config.get('SLACK_START_COMMAND_TOKEN'),
                               team_id=app.config.get('SLACK_TEAM_ID'), methods=['POST'])
                def activate_cameras(**kwargs):
                    for camera in DB.cams.find({}):
                        CameraStateController.change_camera_state(camera, True, user=kwargs.get('user_name'))
                    return slack.response("OK")

            if 'SLACK_STOP_COMMAND_TOKEN' in app.config:
                @slack.command('stop', token=app.config.get('SLACK_STOP_COMMAND_TOKEN'),
                               team_id=app.config.get('SLACK_TEAM_ID'), methods=['POST'])
                def deactivate_cameras(**kwargs):
                    for camera in DB.cams.find({}):
                        CameraStateController.change_camera_state(camera, False, user=kwargs.get('user_name'))
                    return slack.response("OK")
