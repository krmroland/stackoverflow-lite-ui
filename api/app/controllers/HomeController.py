from flask import jsonify, make_response


class HomeController:
    @classmethod
    def index(self):
        return jsonify({"message": "Stack overflow-lite API"})

    @classmethod
    def options(cls, path):
        response = make_response("", 200)
        response.headers.add(
            'Access-Control-Allow-Methods',
            'POST,GET,DELETE,PUT,PATCH'
        )
        response.headers.add(
            'Access-Control-Allow-Headers',
            'content-type,Authorization'
        )

        return response
