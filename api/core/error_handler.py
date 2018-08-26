from flask import jsonify
from jwt.exceptions import ExpiredSignatureError

errors = [

    {
        "code": 405,
        "description": "The method is not allowed for the requested URL."
    }, {
        "code": 408,
        "description": "The server closed the network connection because"
        "the browser didn\'t finish the request within the specified time"
    },
    {
        "code": 500,
        "description": "The server  was unable to complete your request"
    },
    {
        "code": 422
    },
    {
        "code": 401
    },
    {
        "code": 404
    }

]


def _register_error_handler(app, error):
    code = error["code"]

    def error_handler(exception):
        description = error.get("description", exception.description)
        return jsonify(dict(error=description)), code
    app.register_error_handler(code, error_handler)


def token_expired(e):
    return jsonify({"error": "Token has expired"}), 401


def handle_errors(app):
    app.register_error_handler(ExpiredSignatureError, token_expired)
    for error in errors:
        _register_error_handler(app, error)
