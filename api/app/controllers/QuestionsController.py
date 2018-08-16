from flask import jsonify
from api.app.models import Question


class QuestionsController:
    def index(self):
        return jsonify({
            "data": Question.all()
        })
