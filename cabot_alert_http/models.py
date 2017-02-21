from logging import getLogger

import requests
from requests.auth import HTTPBasicAuth

from cabot.cabotapp.alert import AlertPlugin

logger = getLogger(__name__)

# FIXME: Move host and credentials to environment variables (or local settings).
SUPERSET_URL = 'http://127.0.0.1:8088/api/v1/alerts'
SUPERSET_USERNAME = 'user1'
SUPERSET_PASSWORD = 'secret'


class HTTPAlert(AlertPlugin):
    name = 'HTTP'
    slug = 'cabot_alert_http'
    author = 'Kazbek'
    version = '0.0.1'
    font_icon = 'fa fa-code'

    @staticmethod
    def _serialize_check(check):
        return {
            'id': check.id,
            'name': check.name
        }

    def send_alert(self, service, users, duty_officers):

        data = {
            'users': [user.username for user in users],
            'failing_checks': [self._serialize_check(c) for c in service.all_failing_checks],
            'passing_checks': [self._serialize_check(c) for c in service.all_passing_checks],
        }

        resp = requests.post(
            SUPERSET_URL, json=data,
            auth=HTTPBasicAuth(SUPERSET_USERNAME, SUPERSET_PASSWORD))

        if resp.status_code != 201:
            raise Exception(
                'Failed to create check. Status code: {}, body: {}'
                .format(resp.status_code, resp.text))

        return True
