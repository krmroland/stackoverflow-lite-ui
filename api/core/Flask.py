from flask import Flask as BaseFlask, request
from .Request import Request
from .routing.Router import Router
from .JSONEncoder import JSONEncoder
from .commands import migrate_command


class Flask(BaseFlask):
    request_class = Request

    json_encoder = JSONEncoder

    def __init__(self, *args, **kwargs):
        BaseFlask.__init__(self, *args, **kwargs)
        self.cli.add_command(migrate_command)

    def dispatch_request(self):
        """triggers an action related  to this request"""
        adapter = self.create_url_adapter(request)
        name, param = adapter.match()
        if str(name).startswith("static"):
            return BaseFlask.dispatch_request(self)

        return Router.match(name, param)
