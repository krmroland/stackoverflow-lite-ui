from flask import jsonify, request
from api.app.models import Question


class QuestionsController:
    def index(self):
        return jsonify({
            "data": Question.all()
        })

    def store(self):
        return jsonify({
            "data": Question.create(request.validate({
                "title": "required|min_length:3|max_length:50",
                "description": "required|min_length:3|max_length:200"
            }))
        }), 201

    def show(self, id):
        return jsonify({
            "data": Question.find_or_fail(id)
        })
