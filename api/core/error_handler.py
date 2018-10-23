from flask import jsonify
from jwt.exceptions import ExpiredSignatureError, DecodeError

error_codes = set([401, 405, 404, 408, 500])


def _register_error_handler(app, error_code):

    def error_handler(exception):
        return jsonify(dict(message=exception.description)), error_code
    app.register_error_handler(error_code, error_handler)


def token_expired(e):
    return jsonify({"message": "Token has expired"}), 401


def error_token(e):
    return jsonify({"message": "Error decoding token"}), 401


def validation_error(e):
    return jsonify({"message": "Validation Failed", "errors": e.errors}), 422


def handle_errors(app):
    app.register_error_handler(ExpiredSignatureError, token_expired)
    app.register_error_handler(DecodeError, error_token)
    app.register_error_handler(422, validation_error)

    for error_code in error_codes:
        _register_error_handler(app, error_code)
