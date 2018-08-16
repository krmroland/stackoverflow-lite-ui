from api.core import Router
from .controllers import *


Router.group([
    Router.get("/", HomeController, "index"),
    Router.resource("/questions", QuestionsController)
]).prefix("/api/v1.0")
