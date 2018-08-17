from flask import Flask as BaseFlask, request
from .Request import Request
from .routing.Router import Router
from .JSONEncoder import JSONEncoder


class Flask(BaseFlask):
    request_class = Request

    json_encoder = JSONEncoder

    def dispatch_request(self):
        """triggers an action related  to this request"""
        adapter = self.create_url_adapter(request)
        name, param = adapter.match()

        return Router.match(name, param)
