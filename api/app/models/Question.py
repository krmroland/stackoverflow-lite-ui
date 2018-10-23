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
    def get_all_with_authors(cls):
        return User.add_entity_authors(cls.all().to_json())

    @classmethod
    def with_answers(cls, id):
        question = cls.find_or_fail(id)
        author = User.where(id=question.attributes["user_id"]).get(
            ["name", "email"]
        )
        if author:
            author = author[0]

        question.attributes["author"] = author
        question_id = question.attributes.get("id")
        answers = Answer.where(question_id=question_id).get()
        question.attributes["answers"] = User.add_entity_authors(answers)
        return question

    def _creating(self):
        self.attributes["user_id"] = User.auth().id()
