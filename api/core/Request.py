from flask import Request as BaseRequest

from .Validator import Validator


class Request(BaseRequest):

    def all(self):
        if self.is_json:
            return self.get_json()
        return self.values

    def get(self, field, default=None):
        if isinstance(field, list):
            return {key: self._get_field(key) for key in field}
        return self._get_field(field, default)

    def only(self, fields):
        return self.get(fields)

    def _get_field(self, field, default=None):
        return self.all().get(field, default)

    def validate(self, rules):
        return self.get(Validator(self.all()).validate(rules))
