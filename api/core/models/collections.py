
class ModelCollection:
    def __init__(self, models=[]):
        self.models = models

    def count(self):
        return len(self.models)

    def __len__(self):
        return self.count()

    def to_json(self):
        return [model.to_json() for model in self.models]

    def first(self):
        try:
            return self.models[0]
        except IndexError:
            return None

    def __iter__(self):
        return iter(self.models)

    def __repr__(self):
        return str(self.models)
