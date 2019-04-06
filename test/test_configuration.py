import pytest
from api.models.Configuration import CONFIG
from .TestConnexion import TestConnexion


@pytest.mark.usefixtures('client')
class TestConfiguration(TestConnexion):
    """A test to get API token from PrefStore
    """

    def test_getAPIToken(self, client):
        assert CONFIG.getAPItoken() == TestConnexion.WEATHER_API_TOKEN
