from tests.feature import BaseTestCase


class TestQuestions(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.with_authentication()

        self.question = dict(
            title="Whats your take on Joining Andela",
            description="Give a description on what your take on"
            "Joinong andela would be"
        )

    def test_it_returns_a_200_response_for_index_route(self):
        rv = self.get("/questions")
        self.assertEqual(rv.status_code, 200)

    def test_it_returns_all_questions_with_their_authors(self):
        rv = self.post("/questions", self.question)
        rv = self.get("/questions")
        self.assertIn("author", rv.get_json()["data"][0])

    def test_it_returns_a_422_response_for_invalid_data(self):
        rv = self.post("/questions", {})
        self.assertEqual(rv.status_code, 422)

    def test_it_returns_a_201_response_for_valid_data(self):
        rv = self.post("/questions", self.question)
        self.assertEqual(rv.status_code, 201)

    def test_it_returns_a_json_data_with_a_valid_question(self):
        rv = self.post("/questions", self.question)
        self.assertDictContainsSubset(self.question, rv.get_json()["data"])

    def test_it_gives_an_message_with_invalid_data(self):
        rv = self.post("/questions", {})
        data = rv.get_json()
        self.assertEqual(data["message"], "Validation Failed")

    def test_it_returns_a_question_given_an_existing_id(self):
        rv = self.post("/questions", self.question)
        rv = self.get("/questions/1")
        self.assertDictContainsSubset(self.question, rv.get_json()["data"])

    def test_it_fails_getting_a_question_given_a_non_id(self):
        rv = self.get("/questions/1")
        self.assertEqual(rv.status_code, 404)

    def test_it_returns_a_200_status_code_when_deleting_an_existing_id(self):
        self.post("/questions", self.question)
        rv = self.delete("/questions/1")
        self.assertEqual(rv.status_code, 200)

    def test_it_returns_a_404_status_code_when_deleting_an_non_id(self):
        rv = self.delete("/questions/1")
        self.assertEqual(rv.status_code, 404)

    def test_it_updates_an_existing_question(self):
        self.post("/questions", self.question)
        update = dict(title="Updated title", description="Updated description")
        self.question.update(update)
        rv = self.patch("/questions/1", update)
        self.assertEqual(rv.status_code, 200)
        data = rv.get_json()["data"]
        self.assertEqual(data["title"], self.question["title"])

    def test_returns_a_401_response_when_deleting_others_question(self):
        self.post("/questions", self.question)
        self.login(self.user_two)
        rv = self.delete("/questions/1")
        self.assertEqual(rv.status_code, 401)

    def test_returns_a_401_when_updating_others_users_question(self):
        self.post("/questions", self.question)
        self.login(self.user_two)
        update = dict(title="Updated title", description="Updated description")
        self.question.update(update)
        rv = self.patch("/questions/1", update)
        self.assertEqual(rv.status_code, 401)
