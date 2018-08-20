from flask import jsonify


def validation_exception(e):
    return jsonify(e.response), 422


def not_found_exception(e):
    response = e.response or dict(error="Resource doesn't exist")
    return jsonify(response), 404


def handle_errors(app):
    app.register_error_handler(422, validation_exception)
    app.register_error_handler(404, not_found_exception)
