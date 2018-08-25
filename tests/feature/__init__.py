from unittest import TestCase
from api.app import create_app
from api.core.commands import migrate


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.url_prefix = "api"
        self.api_version = "v1.0"
        with self.app.app_context():
            migrate()

    def tearDown(self):
        pass

    def get(self, url):
        return self.client.get(**self._make_options(url))

    def post(self, url, json=None):
        return self.client.post(**self._make_options(url, json))

    def patch(self, url, json=None):
        return self.client.patch(**self._make_options(url, json))

    def put(self, url, json=None):
        return self.client.put(**self._make_options(url, json))

    def delete(self, url):
        return self.client.delete(**self._make_options(url))

    def _base_url(self, url):
        return f"/{self.url_prefix}/{self.api_version}{url}"

    def _make_options(self, url, json=None):
        options = dict(path=self._base_url(url))
        if json:
            options["json"] = json
        return options
