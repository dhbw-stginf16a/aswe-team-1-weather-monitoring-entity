#!/usr/bin/env python3

import logging
import requests
from api.models.Configuration import CONFIG

logger = logging.getLogger(__name__)

class PrefStoreClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_global_prefs(self):
        r = requests.get("{}/preferences/global/".format(self.base_url))
        assert r.status_code == 200
        return r.json()

PREFSTORE_CLIENT = PrefStoreClient(CONFIG.CENTRAL_NODE_BASE_URL)

