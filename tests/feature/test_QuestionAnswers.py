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

    def test_add_a_question_answer_returns_a_201_status(self):
        rv = self.post(self.answers_url(), dict(body="Some answer"))
        self.assertEqual(201, rv.status_code)

    def test_add_a_question_answer_passes(self):
        answer = dict(body="Some answer")
        rv = self.post(self.answers_url(), answer)
        self.assertDictContainsSubset(answer, rv.get_json()["data"])

    def test_add_a_question_answer_fails_with_invalid_data(self):
        rv = self.post(self.answers_url())
        self.assertEqual(rv.status_code, 422)

    def test_get_existing_question_answer_returns_a_200_response(self):
        self.post(self.answers_url(), dict(body="Some existing answer"))
        rv = self.get(self.answer_url(1))
        self.assertEqual(rv.status_code, 200)

    def test_it_updates_an_existing_question_answer(self):
        self.post(self.answers_url(), dict(body="Some existing answer"))
        update = dict(body="Updated answer")
        rv = self.put(self.answer_url(1), update)
        answer = rv.get_json()["data"]
        self.assertDictContainsSubset(update, answer)

    def test_it_deletes_an_existing_question(self):
        self.post(self.answers_url(), dict(body="Some existing answer"))
        self.delete(self.answer_url(1))
        rv = self.get(self.answer_url(1))
        self.assertEqual(rv.status_code, 404)
