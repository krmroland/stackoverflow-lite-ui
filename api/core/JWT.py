import jwt
from flask import current_app
from datetime import datetime, timedelta


class JWT:
    _secret = None

    @classmethod
    def generate_token(cls, email):
        expires = datetime.utcnow() + timedelta(seconds=30)

        token = jwt.encode(
            {'email': email, 'exp': expires},
            cls._get_secret(),
            algorithm='HS256',

        )

        return {"token": token.decode("UTF-8")}

    @classmethod
    def _get_secret(cls):
        if not cls._secret:
            cls._secret = current_app.config.get("SECRET")
        return cls._secret
