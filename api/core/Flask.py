from flask import Flask as BaseFlask, request
from .routing.Router import Router


class Flask(BaseFlask):

    def dispatch_request(self):
        """triggers an action related  to this request"""
        adapter = self.create_url_adapter(request)
        name, param = adapter.match()

        return Router.match(name, param)
