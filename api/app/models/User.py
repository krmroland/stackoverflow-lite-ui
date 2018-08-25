from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from api.core.models import Model
from api.core import JWT


class User(Model):
    hidden = ["password"]

    @classmethod
    def table_name(cls):
        return "users"

    def _creating(self):
        password = self.attributes["password"]
        self.attributes["password"] = generate_password_hash(password)

    @classmethod
    def authenticate(cls, credentials):
        data = cls.where(email=credentials["email"]).first()
        if data and User(data)._password_matches(credentials["password"]):
            return JWT().generate_token(data["email"])
        return abort(401, "Invalid login credentials")

    def _password_matches(self, password):
        return check_password_hash(self.attributes["password"], password)
