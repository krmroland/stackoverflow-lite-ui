from tests.feature import BaseTestCase


class TestAuthentication(BaseTestCase):
    def setUp(self):

        super().setUp()

        self.user_fields = {
            "name": "Ahimbsisibwe Roland",
            "email": "rolandmbasa@gmail.com",
            "password": "password",
            "password_confirmation": "password"
        }

        self.login_credentials = {
            "email": "rolandmbasa@gmail.com",
            "password": "password",
        }

    def test_registration_returns_a_422_response_with_invalid_data(self):
        rv = self.post("/auth/signup")
        self.assertEqual(rv.status_code, 422)

    def test_registration_returns_a_200_response_with_a_valid_data(self):
        rv = self.create_user()
        self.assertEqual(rv.status_code, 200)

    def test_registration_fails_with_an_existing_email(self):
        rv = self.create_user()
        rv = self.create_user()
        self.assertIn("email", rv.get_json()["errors"])

    # def test_registration_response_doesnot_include_password_field(self):
    #     rv = self.create_user()
    #     self.assertNotIn("password", rv.get_json()["data"])

    def test_login_returns_a_422_response_with_no_data(self):
        rv = self.post("/auth/login")
        self.assertEqual(rv.status_code, 422)

    def test_login_returns_a_422_response_with_invalid_credentials(self):
        rv = self.post("/auth/login", self.login_credentials)
        self.assertEqual(rv.status_code, 422)

    def test_login_returns_a_token_with_valid_credentials(self):
        self.create_user()
        rv = self.post("/auth/login", self.login_credentials)
        self.assertIn("token", rv.get_json())

    def test_login_fails_with_an_invalid_password(self):
        self.create_user()

        wrong_credentials = {
            "email": "rolandmbasa@gmail.com",
            "password": "Wrong password"
        }

        rv = self.post("/auth/login", wrong_credentials)
        self.assertEqual(rv.status_code, 422)

    def test_protected_route_fails_without_authentication(self):
        rv = self.get("/questions")
        self.assertEqual(rv.status_code, 401)

    def create_user(self):
        return self.post("/auth/signup", self.user_fields)
