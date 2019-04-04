from datetime import datetime
import pytest
import requests

from .TestConnexion import TestConnexion
from freezegun import freeze_time


@pytest.mark.usefixtures('client')
class TestRequest(TestConnexion):
    """A test to get events from the calendar api
    """

    @pytest.fixture(scope='function')
    def test_getEventsDay(self, client):
        request = {
            'type': 'weather_current',
            'payload': {
                'user': 'AntonHynkel',
                'date': '2007-11-01'
            }
        }

        response = client.post('api/v1/request', json=request)

        assert response.status_code == 200

    def test_getEventsTimerange(self, client):
        request = {
            'type': 'event_timerange',
            'payload': {
                'user': 'AntonHynkel',
                'startDate': '2007-01-01',
                'endDate':  '2007-12-31'
            }
        }

        response = client.post('api/v1/request', json=request)

        assert response.status_code == 200
        print(response.get_json())


    @freeze_time("2019-04-01 10:00:00") # UTC Timestamp: 1554112800
    def test_getOutdatedForecast(self, client):
        request = {
            'type': 'weather_forecast',
            'payload': {
                'time': '1554111800',
                'location':  'Stuttgart, de'
            }
        }
        response = client.post('api/v1/request', json=request)

        assert response.status_code == 500
