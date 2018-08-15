from unittest import TestCase
from api.app import create_app


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
