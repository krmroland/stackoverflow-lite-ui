from flask import jsonify
from api.core.exceptions import ValidationException


def validation_exception(e):
    return jsonify(dict(message="Validation Failed", errors=e.errors)), 422


def handle_errors(app):
    app.register_error_handler(ValidationException, validation_exception)
