from api.tests import BaseTestCase


class TestHomeController(BaseTestCase):
    def test_it_successfully_loads_the_index_route(self):
        rv = self.client.get("api/v1.0/")
        self.assertEquals(rv.status_code, 200)
