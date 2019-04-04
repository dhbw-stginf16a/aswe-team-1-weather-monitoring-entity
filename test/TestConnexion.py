import pytest
import os

from app import app


class TestConnexion:
    """The base test providing auth and flask clients to other tests
    """
    cache: dict = {}
    CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')
    WEATHER_API_TOKEN = "ImAnAPIToken"

    @pytest.fixture(scope='function')
    def client(self, requests_mock):
        globalPrefs = {
            "weather_monitor/api_token": self.WEATHER_API_TOKEN
        }

        requests_mock.get(f'{self.CENTRAL_NODE_BASE_URL}/preferences/global/', status_code=200, json=globalPrefs)
        with app.app.test_client() as c:
            yield c
