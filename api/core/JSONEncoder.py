from flask.json import JSONEncoder as BaseJSONEncoder
from api.core.storage import Model, ModelCollection


class JSONEncoder(BaseJSONEncoder):
    def default(self, data):
        if isinstance(data, Model) or isinstance(data, ModelCollection):
            return data.to_json()
        return BaseJSONEncoder.default(self, data)
