from api.core import Flask
from api.config import config
from api.app.routes import Router
from api.core.error_handler import handle_errors


def load_routes(app):
    for route in Router.routes:
        app.url_map.add(Router.register_route(route))


def add_cors_support(app):
    @app.after_request
    def after_every_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(config[environment])

    load_routes(app)

    handle_errors(app)

    add_cors_support(app)

    return app
