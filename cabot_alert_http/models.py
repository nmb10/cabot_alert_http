from logging import getLogger

import requests
from requests.auth import HTTPBasicAuth

from cabot.cabotapp.alert import AlertPlugin

logger = getLogger(__name__)

# FIXME: Move host and credentials to environment variables (or local settings).
SUPERSET_URL = 'http://127.0.0.1:8088/api/v1/alerts-consumer'
SUPERSET_USERNAME = 'user1'
SUPERSET_PASSWORD = 'secret'


class HTTPAlert(AlertPlugin):
    name = 'HTTP'
    slug = 'cabot_alert_http'
    author = 'Kazbek'
    version = '0.0.1'
    font_icon = 'fa fa-code'

    def send_alert(self, service, users, duty_officers):
        message = service.get_status_message()
        data = {
            'users': [user.username for user in users],
            'message': str(message),
        }

        resp = requests.post(
            SUPERSET_URL, json=data,
            auth=HTTPBasicAuth(SUPERSET_USERNAME, SUPERSET_PASSWORD))

        if resp.status_code != 201:
            raise Exception(
                'Failed to create check. Status code: {}, body: {}'
                .format(resp.status_code, resp.text))

        return True
