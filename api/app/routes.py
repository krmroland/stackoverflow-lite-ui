from api.core import Router
from .controllers import *


Router.group([
    Router.get("/", HomeController, "index"),
    Router.resource("/questions", HomeController)
]).prefix("/api/v1.0")
