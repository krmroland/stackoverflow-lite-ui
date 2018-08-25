from datetime import datetime, timedelta

import jwt
from flask import current_app


class JWT:
    def __init__(self, algorithm="HS256"):
        self.secret = current_app.config.get("SECRET")
        self.expires = datetime.utcnow() + timedelta(seconds=30)
        self.algorithm = algorithm

    def generate_token(self, email):
        token = jwt.encode(
            {'email': email, 'exp': self.expires},
            self.secret,
            self.algorithm
        )
        return {"token": token.decode("UTF-8")}
