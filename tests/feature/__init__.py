from unittest import TestCase
from api.app import create_app
from api.core.commands import migrate


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.url_prefix = "api"
        self.api_version = "v1.1"
        self.auth_token = None
        self.user_one = dict({
            "name": "Ahimbisibwe Roland",
            "email": "lonusroland@gmail.com",
        })
        self.user_two = dict({
            "name": "Nabaasa Richard",
            "email": "nabrick@gmail.com",
        })
        with self.app.app_context():
            migrate()

    def tearDown(self):
        pass

    def get(self, url):
        return self.client.get(**self._make_options(url))

    def options(self, url):
        return self.client.options(**self._make_options(url))

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
        if self.auth_token:
            headers = dict(Authorization=f"Bearer {self.auth_token}")
            options["headers"] = headers
        return options

    def with_authentication(self):
        self.login()

    def login(self, user=None):
        if not user:
            user = self.user_one

        user["password"] = "password"
        user["password_confirmation"] = "password"

        rv = self.post("/auth/signup", user)
        # ensure registration passed since Flask doesn't handle errors
        # during testing

        assert rv.status_code == 201

        rv = self.post("/auth/login", user)

        assert rv.status_code == 200

        self.auth_token = rv.get_json().get("token")
