from api.core.models import Model
from .Answer import Answer
from .User import User


class Question(Model):
    @classmethod
    def table_name(cls):
        return "questions"

    def answers(self):
        return self.has_many(Answer)

    @classmethod
    def with_answers(cls, id):
        question = cls.find_or_fail(id)
        question_id = question.attributes.get("id")
        question.attributes["answers"] = Answer.where(
            question_id=question_id
        ).get()
        return question

    def _creating(self):
        self.attributes["user_id"] = User.auth().id()
