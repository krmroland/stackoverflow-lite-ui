from flask import Flask
from api.config import config


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(config[environment])

    return app
