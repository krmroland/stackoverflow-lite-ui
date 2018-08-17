from flask import jsonify


class HomeController:
    @classmethod
    def index(self):
        return jsonify({"message": "Stack overflow-lite API"})
