from api.core.storage import Model
from .Answer import Answer


class Question(Model):
    def answers(self):
        return self.has_many(Answer)
