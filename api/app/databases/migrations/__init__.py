from .Questions import QuestionsTable, AnswersTable
from .User import UsersTable

migrations = [UsersTable(), QuestionsTable(), AnswersTable()]

__all__ = ["migrations"]
