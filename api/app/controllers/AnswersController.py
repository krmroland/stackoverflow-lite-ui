from flask import jsonify, request
from api.app.models import Question, Answer, User
from .BaseController import ProtectedController


class AnswersController(ProtectedController):
    @classmethod
    def index(cls, question_id):
        question = Question.find_or_fail(question_id).load("answers")
        return jsonify(dict(data=question["answers"]))

    @classmethod
    def show(cls, question_id, answer_id):
        answer = Answer.by_question_id(question_id, answer_id).first_or_fail()
        return jsonify(dict(data=answer)), 200

    @classmethod
    def store(cls, question_id):
        question = Question.find_or_fail(question_id)
        answer = question.answers().create(request.validate({
            "body": "required"
        }))
        return jsonify(dict(data=answer)), 201

    @classmethod
    def update(cls, question_id, answer_id):
        answer = Answer.find_or_fail(answer_id)
        if User.owns_answer(answer):
            answer.update(request.validate({"body": "required"}))
            return jsonify(dict(data=answer)), 200

        question = Question.find_or_fail(question_id)

        if User.owns_question(question):
            question.update(dict(answer_id=answer_id))
            return jsonify(
                dict(message="Answer marked as the preferred")
            ), 200

        return jsonify(dict(error="Access denied for updating answer")), 401

    @classmethod
    def destroy(cls, question_id, answer_id):
        answer = Answer.find_or_fail(answer_id)
        if not User.owns_answer(answer):
            return jsonify(dict(error="Access denied")), 401
        answer.delete()
        return jsonify(dict(message="Answer was successively removed")), 200
