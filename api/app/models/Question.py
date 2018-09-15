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
        questions = cls.all()
        if not questions:
            return questions
        user_ids = [qtn.attributes['user_id'] for qtn in questions]
        users = User.where_in("id", user_ids).get(["id", "name"])
        user_map = {user["id"]: user for user in users}
        for qtn in questions:
            qtn.attributes["author"] = user_map.get(qtn["user_id"])
        return questions

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
