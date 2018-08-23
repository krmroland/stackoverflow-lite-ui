from .Questions import QuestionsTable, AnswersTable

migrations = [QuestionsTable(), AnswersTable()]

__all__ = ["migrations"]
