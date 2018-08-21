from flask import jsonify

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
]


def _json_error(code, description):
    def error_handler(e):
        return jsonify(dict(error=description)), code
    return error_handler


def validation_exception(e):
    return jsonify(e.response), 422


def not_found_exception(e):
    response = e.response or dict(error="Resource doesn't exist")
    return jsonify(response), 404


def _register_generic_errors(app):
    for error in errors:
        app.register_error_handler(
            error["code"],
            _json_error(error["code"], error["description"])
        )


def handle_errors(app):
    app.register_error_handler(422, validation_exception)
    app.register_error_handler(404, not_found_exception)
    _register_generic_errors(app)
