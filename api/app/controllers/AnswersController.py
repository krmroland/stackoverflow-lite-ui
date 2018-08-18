from flask import jsonify
from api.app.models import Question


class AnswersController:
    @classmethod
    def index(cls, question_id):
        question = Question.find_or_fail(question_id).load("answers")
        return jsonify(dict(data=question["answers"]))
