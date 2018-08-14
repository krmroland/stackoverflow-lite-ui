from api.core import Router
from .controllers import *


Router.group([
    Router.get("/", HomeController, "index"),
]).prefix("/api/v1.0")
