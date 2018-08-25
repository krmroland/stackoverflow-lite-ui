from unittest import TestCase
from api.core.Validator import Validator
from api.core.exceptions import ValidationException


class TestValidation(TestCase):

    def test_required_fails(self):
        validator = Validator({})
        self.assert_fails(validator, {"name": "required"})
        self.assertIn("name", validator.errors)

    def test_required_passes(self):
        validator = Validator(dict(name="Roland"))
        validator.validate({"name": "required"})
        self.assertNotIn("name", validator.errors)

    def test_length_fails(self):
        validator = Validator(dict(name="Roland"))
        self.assert_fails(validator, {"name": "length:10"})
        self.assertIn("name", validator.errors)

    def test_lenght_passes(self):
        validator = Validator(dict(name="Roland"))
        validator.validate({"name": "length:6"})
        self.assertNotIn("name", validator.errors)

    def test_min_length_fails(self):
        validator = Validator(dict(name="Roland"))
        self.assert_fails(validator, {"name": "min_length:15"})
        self.assertIn("name", validator.errors)

    def test_min_lenght_passes(self):
        validator = Validator(dict(name="Ahimbisibwe Roland"))
        validator.validate({"name": "min_length:10"})
        self.assertNotIn("name", validator.errors)

    def test_max_length_fails(self):
        validator = Validator(dict(name="Roland"))
        self.assert_fails(validator, {"name": "max_length:3"})
        self.assertIn("name", validator.errors)

    def test_max_lenght_passes(self):
        validator = Validator(dict(name="Andela"))
        validator.validate({"name": "max_length:10"})
        self.assertNotIn("name", validator.errors)

    def test_validate_email_fails(self):
        validator = Validator(dict(email="some_invald_email"))
        self.assert_fails(validator, {"email": "email"})
        self.assertIn("email", validator.errors)

    def test_validate_email_passes(self):
        validator = Validator(dict(email="someone@andela.com"))
        validator.validate({"email": "email"})
        self.assertNotIn("email", validator.errors)

    def test_validate_confirmed_fails(self):
        validator = Validator(
            dict(password="secret", password_confirmation="password")
        )
        self.assert_fails(validator, {"password": "confirmed"})
        self.assertIn("password", validator.errors)

    def test_validate_confirmed_passed(self):
        validator = Validator(
            dict(password="secret", password_confirmation="secret")
        )
        validator.validate({"password": "confirmed"})
        self.assertNotIn("password", validator.errors)

    def assert_fails(self, validator, data):
        self.assertRaises(ValidationException, validator.validate, data)
