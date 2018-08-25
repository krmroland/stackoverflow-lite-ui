from .Questions import QuestionsTable, AnswersTable
from .User import UsersTable

migrations = [QuestionsTable(), AnswersTable(), UsersTable()]

__all__ = ["migrations"]
