from api.app.models import User


class ProtectedController:

    def __init__(self):
        self.middleware("auth_midleware")

    def middleware(self, middleware):
        return getattr(self, middleware)()

    @classmethod
    def auth_midleware(cls):
        return User.auth().is_authenticated()
