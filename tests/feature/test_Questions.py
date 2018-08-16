from tests.feature import BaseTestCase


class TestQuestions(BaseTestCase):
    def test_it_returns_a_200_response_for_index_route(self):
        rv = self.get("/questions")
        self.assertEqual(rv.status_code, 200)
