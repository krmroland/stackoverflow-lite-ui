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

    def assert_fails(self, validator, data):
        self.assertRaises(ValidationException, validator.validate, data)
