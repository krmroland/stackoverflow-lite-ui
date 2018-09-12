from api.core import Router
from .controllers import *


Router.group([
    Router.get("/", HomeController, "index"),
    Router.resource("/questions", QuestionsController),
    Router.resource("/questions.answers", AnswersController),
    Router.post("/auth/signup", AuthController, "sign_up"),
    Router.post("/auth/login", AuthController, "login"),
    Router.options("/<path:anything>", HomeController, "options")
]).prefix("/api/v1.1")
