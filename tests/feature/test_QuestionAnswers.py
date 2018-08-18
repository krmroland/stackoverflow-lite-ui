from tests.feature import BaseTestCase


class TestQuestionAnswers(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.question = dict(
            title="Travis CI",
            description="How do I integrate Travis"
        )
        self.add_question()

    def add_question(self):
        rv = self.post("/questions", self.question)
        self.api_question = rv.get_json()["data"]

    def answers_url(self, id=""):
        return f"/questions/{self.api_question['id']}/answers"

    def answer_url(self, id):
        return f"{self.answers_url()}/{id}"

    def test_it_fetches_a_list_of_all_answers(self):
        rv = self.get(self.answers_url())
        self.assertEqual(200, rv.status_code)
