from flask import request, jsonify
from api.app.models import User


class AuthController:
    def sign_up(self):
        data = request.validate({
            "email": "required|email|unique:users",
            "password": "required|min_length:6|confirmed",
            "name": "required|min_length:3"
        })
        User.create({** data})

        return self.authenticate_response(data)

    def login(self):
        data = request.validate({
            "email": "required|email",
            "password": "required|min_length:6",
        })
        return self.authenticate_response(data)

    @classmethod
    def authenticate_response(cls, data):
        response = User.auth().issue_token(data)
        response["message"] = "Authentication was successful"
        return jsonify(response)
