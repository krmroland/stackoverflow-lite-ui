from tests.feature import BaseTestCase


class TestHomeController(BaseTestCase):
    def test_it_successfully_loads_the_index_route(self):
        rv = self.get("/")
        self.assertEquals(rv.status_code, 200)

    def test_it_supports_cross_origin_resource_sharing(self):
        rv = self.options("/some/random/path")
        self.assertEquals(
            rv.headers.get("Access-Control-Allow-Headers"),
            "content-type"
        )
