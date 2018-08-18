from flask import jsonify, request
from api.app.models import Question


class AnswersController:
    @classmethod
    def index(cls, question_id):
        question = Question.find_or_fail(question_id).load("answers")
        return jsonify(dict(data=question["answers"]))

    @classmethod
    def store(cls, question_id):
        question = Question.find_or_fail(question_id)
        answer = question.answers().create(request.validate({
            "body": "required"
        }))
        return jsonify(dict(data=answer)), 201
