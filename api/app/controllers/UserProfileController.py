from flask import jsonify
from .ProtectedController import ProtectedController
from api.app.models.User import Auth
from api.app.models import Question, Answer


class UserProfileController(ProtectedController):
    @classmethod
    def index(cls):
        """Gets the profile data of the authenticated user"""
        user = Auth._User
        query = """
         SELECT questions.title, questions.id,questions.created_at,
         count(answers.*) AS answer_count FROM questions
         LEFT JOIN answers ON  questions.id=answers.question_id
         GROUP BY questions.title, questions.id,questions.created_at
        """
        questions = Question.query().raw(query)
        best_answer_awards = Question.query().raw(f"""
         SELECT count(*) from questions
         LEFT JOIN answers on questions.id=answers.question_id
         WHERE prefered_answer_id IS NOT NULL
         AND  answers.user_id={user.attributes['id']}
        """)
        user.attributes["questions"] = questions
        user.attributes["answer_count"] = Answer.count_for_user(user)
        user.attributes["best_answer_awards"] = best_answer_awards[0]["count"]

        return jsonify(user)
