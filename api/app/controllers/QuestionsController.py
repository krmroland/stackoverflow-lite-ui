from flask import jsonify, request
from api.app.models import Question

validation_rules = {
    "title": "required|min_length:3|max_length:50",
    "description": "required|min_length:3|max_length:200"
}


class QuestionsController:
    def index(self):
        return jsonify({
            "data": Question.all()
        })

    def store(self):
        return jsonify({
            "data": Question.create(request.validate(validation_rules))
        }), 201

    def show(self, id):
        return jsonify({
            "data": Question.find_or_fail(id)
        })

    def update(self, id):
        return jsonify({
            "data": Question.find_or_fail(id).update(
                request.validate(validation_rules)
            )
        })

    def destroy(self, id):
        Question.find_or_fail(id).delete()
        return jsonify(dict(message="Resource was removed successfully"))
