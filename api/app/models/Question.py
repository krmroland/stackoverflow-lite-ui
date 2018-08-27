from api.core.models import Model
from .Answer import Answer
from .User import Auth


class Question(Model):
    @classmethod
    def table_name(cls):
        return "questions"

    def answers(self):
        return self.has_many(Answer)

    def _creating(self):
        self.attributes["user_id"] = Auth.id()
