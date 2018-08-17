from flask import jsonify


def validation_exception(e):
    return jsonify(e.response), 422


def handle_errors(app):
    app.register_error_handler(422, validation_exception)
