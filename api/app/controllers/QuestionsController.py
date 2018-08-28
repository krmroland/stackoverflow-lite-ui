from flask import jsonify, request
from api.app.models import Question, User
from .ProtectedController import ProtectedController

validation_rules = {
    "title": "required|min_length:3|max_length:50",
    "description": "required|min_length:3|max_length:200"
}


class QuestionsController(ProtectedController):
    @classmethod
    def index(cls):
        return jsonify({
            "data": Question.all()
        })

    @classmethod
    def store(cls):
        return jsonify({
            "data": Question.create(request.validate(validation_rules))
        }), 201

    @classmethod
    def show(cls, id):
        return jsonify({
            "data": Question.find_or_fail(id)
        })

    @classmethod
    def update(cls, id):
        question = Question.find_or_fail(id)
        if not User.owns_question(question):
            return jsonify({
                "error": "Access denied for updating question"
            }), 401

        return jsonify({
            "data": question.update(
                request.validate(validation_rules)
            )
        })

    @classmethod
    def destroy(cls, id):
        question = Question.find_or_fail(id)
        if not User.owns_question(question):
            return jsonify(dict(
                error="Access denied  to delete question"
            )), 401
        question.delete()
        return jsonify(dict(message="Resource was removed successfully"))
