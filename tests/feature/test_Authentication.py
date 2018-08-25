from tests.feature import BaseTestCase


class TestAuthentication(BaseTestCase):
    def setUp(self):

        super().setUp()
        self.user = {
            "name": "Ahimbsisibwe Roland",
            "email": "rolandmbasa@gmail.com",
            "password": "password",
            "password_confirmation": "password"
        }

    def test_returns_a_422_response_with_invalid_data(self):
        rv = self.post("/auth/register")
        self.assertEqual(rv.status_code, 422)

    def test_returns_a_201_response_with_a_valid_data(self):
        rv = self.post("/auth/register", self.user)
        self.assertEqual(rv.status_code, 201)

    def test_registration_fails_with_an_existing_email(self):
        rv = self.post("/auth/register", self.user)
        rv = self.post("/auth/register", self.user)
        self.assertIn("email", rv.get_json()["errors"])

    def test_response_doesnot_include_password_field(self):
        rv = self.post("/auth/register", self.user)
        self.assertNotIn("password", rv.get_json()["data"])
