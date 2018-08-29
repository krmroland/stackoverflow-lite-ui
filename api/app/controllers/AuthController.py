from flask import request, jsonify
from api.app.models import User


class AuthController:
    @classmethod
    def sign_up(cls):
        data = request.validate({
            "email": "required|email|unique:users",
            "password": "required|min_length:6|confirmed",
            "name": "required|min_length:3"
        })
        return jsonify(dict(data=User.create(data))), 201

    @classmethod
    def login(cls):
        data = request.validate({
            "email": "required|email",
            "password": "required|min_length:6",
        })

        return jsonify(
            {
                "token": User.auth().issue_token(data),
                "message": "Authentication was successful"
            }
        )
