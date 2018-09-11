from tests.feature import BaseTestCase


class TestHomeController(BaseTestCase):
    def test_it_successfully_loads_the_index_route(self):
        rv = self.get("/")
        self.assertEquals(rv.status_code, 200)
