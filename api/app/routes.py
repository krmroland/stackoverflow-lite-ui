from api.core import Router
from .controllers import *


Router.group([
    Router.get("/", HomeController, "index"),
    Router.resource("/questions", QuestionsController),
    Router.resource("/questions.answers", AnswersController),
    Router.post("/auth/register", AuthController, "register"),
    Router.post("/auth/login", AuthController, "login")
]).prefix("/api/v1.0")
