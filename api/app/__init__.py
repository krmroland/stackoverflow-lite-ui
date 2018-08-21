from api.core import Flask
from api.config import config
from api.app.routes import Router
from api.core.error_handler import handle_errors


def load_routes(app):
    for route in Router.routes:
        app.url_map.add(Router.register_route(route))


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(config[environment])

    load_routes(app)

    handle_errors(app)

    return app
