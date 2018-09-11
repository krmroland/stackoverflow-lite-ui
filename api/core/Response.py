from flask import Response as BaseResponse


class Response(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self.headers.add("Access-Control-Allow-Origin:", "*")
