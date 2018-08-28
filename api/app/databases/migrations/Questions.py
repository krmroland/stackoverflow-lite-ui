from api.core.db.Migration import Migration, TableSchema


class QuestionsTable(Migration):

    def up(self):
        table = TableSchema.create("questions")
        table.increments("id")
        table.integer("user_id")
        table.string("title", 100)
        table.text("description")
        table.timestamps()

    def down(self):
        TableSchema.drop_if_exists("questions")


class AnswersTable(Migration):
    def up(self):
        table = TableSchema.create("answers")
        table.increments("id")
        table.text("body")
        table.integer("question_id")
        table.integer("user_id")
        table.timestamps()

    def down(self):
        TableSchema.drop_if_exists("answers")
