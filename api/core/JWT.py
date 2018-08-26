from datetime import datetime, timedelta
from flask import current_app, request, abort
import jwt


class JWT:
    def __init__(self, algorithm="HS256"):
        self.secret = current_app.config.get("SECRET")
        self.expires = datetime.utcnow() + timedelta(minutes=15)
        self.algorithm = algorithm

    def _make_options(self):
        return dict(key=self.secret, algorithm=self.algorithm)

    def generate_token(self, subject):
        return jwt.encode(
            {'subject': subject, 'exp': self.expires},
            **self._make_options(),
        ).decode("UTF-8")

    def get_subject_from_headers(self):
        token = self.get_token_from_header()
        return jwt.decode(token, **self._make_options())["subject"]

    @classmethod
    def get_token_from_header(cls):
        token = str(request.headers.get("AUTHORIZATION"))
        parts = token.split()
        if len(parts) == 2 and parts[0] == "Bearer":
            return str(parts[1]).strip()
        return abort(401)
