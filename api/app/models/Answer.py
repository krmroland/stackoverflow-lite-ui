from api.core.models import Model
from .User import User


class Answer(Model):
    @classmethod
    def table_name(cls):
        return "answers"

    @classmethod
    def by_question_id(cls, qtn_id, ans_id):
        return cls.where(question_id=qtn_id, id=ans_id)

    def _creating(self):
        self.attributes["user_id"] = User.auth().id()
