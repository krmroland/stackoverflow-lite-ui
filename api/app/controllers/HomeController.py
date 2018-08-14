from flask import jsonify


class HomeController:
    def index(self):
        return jsonify({"message": "Stack overflow-lite API"})
