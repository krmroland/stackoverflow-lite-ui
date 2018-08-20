from flask.json import JSONEncoder as BaseJSONEncoder
from api.core.storage import Model, ModelCollection


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, Model) or isinstance(o, ModelCollection):
            return o.to_json()
        return JSONEncoder.default(self, o)  # pragma: no cover
