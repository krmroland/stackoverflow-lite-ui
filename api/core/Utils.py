from datetime import datetime


def time_now():
    return datetime.now()
    # return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Fluent:
    def __init__(self, attributes={}):
        self.set_attributes(attributes)

    def update(self, attributes):
        self.attributes.update(attributes)

    def set_attributes(self, attributes):
        object.__setattr__(self, "attributes", attributes)

    def __getattr__(self, key):
        return self.attributes.get(key, None)

    def __getitem__(self, key):
        return self.attributes.get(key, None)

    def __setattr__(self, key, value):
        self.attributes[key] = value

    def __repr__(self):
        return str(self.attributes)

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __iter__(self):
        return iter(self.attributes)
