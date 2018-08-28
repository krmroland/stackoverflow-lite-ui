from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from api.core.models import Model
from api.core import JWT


class Auth:
    user = None

    def __init__(self, UserModel):
        self.UserModel = UserModel
        self.jwt = JWT()

    def authenticate(self, credentials):
        user = self.get_user(credentials["email"])
        if not user._password_matches(credentials["password"]):
            return abort(401, "Invalid login credentials")
        return self.jwt.generate_token(user.attributes["email"])

    def is_authenticated(self):
        Auth.user = self.get_user(self.jwt.get_subject_from_headers())
        return True

    def get_user(self, email):
        data = self.UserModel.where(email=email).first()
        if not data:
            return abort(401, "Email Address not found")
        return self.UserModel(data)

    @classmethod
    def id(cls):
        if cls.user:
            return cls.user.attributes["id"]
        abort(401, "User is not signed in")  # pragma: no cover


class User(Model):
    hidden = ["password"]

    @classmethod
    def table_name(cls):
        return "users"

    def _creating(self):
        password = self.attributes["password"]
        self.attributes["password"] = generate_password_hash(password)

    def _password_matches(self, password):
        return check_password_hash(self.attributes["password"], password)

    @classmethod
    def owns_question(cls, question):
        return cls.entity_belongs_to_user(question)

    @classmethod
    def owns_answer(cls, answer):
        return cls.entity_belongs_to_user(answer)

    @classmethod
    def entity_belongs_to_user(cls, entity, attribute="user_id"):
        user_id = Auth.id()
        return user_id and user_id == entity.get_attribute(attribute)

    @classmethod
    def auth(cls):
        return Auth(cls)
