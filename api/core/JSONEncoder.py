from flask.json import JSONEncoder as BaseJSONEncoder
from api.core.models import Model
from api.core.models.collections import ModelCollection
from datetime import datetime


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, Model) or isinstance(o, ModelCollection):
            return o.to_json()
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return JSONEncoder.default(self, o)  # pragma: no cover
