from api.core.models import Model
from werkzeug.security import generate_password_hash


class User(Model):
    hidden = ["password"]

    def table_name():
        return "users"

    def _creating(self):
        password = self.attributes["password"]
        self.attributes["password"] = generate_password_hash(password)
