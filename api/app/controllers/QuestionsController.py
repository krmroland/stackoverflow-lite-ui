from flask import jsonify, request
from api.app.models import Question

validation_rules = {
    "title": "required|min_length:3|max_length:50",
    "description": "required|min_length:3|max_length:200"
}


class QuestionsController:
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
        return jsonify({
            "data": Question.find_or_fail(id).update(
                request.validate(validation_rules)
            )
        })

    @classmethod
    def destroy(cls, id):
        Question.find_or_fail(id).delete()
        return jsonify(dict(message="Resource was removed successfully"))
