from api.core.db.Migration import Migration, TableSchema


class QuestionsTable(Migration):

    def up(self):
        table = TableSchema.create("questions")
        table.increments("id")
        table.integer("user_id").references("id").on_table("users")
        table.string("title", 100)
        table.text("description")
        table.integer("answer_id").nullable()
        table.timestamps()

    def down(self):
        TableSchema.drop_if_exists("questions")


class AnswersTable(Migration):
    def up(self):
        table = TableSchema.create("answers")
        table.increments("id")
        table.text("body")
        table.integer("question_id").references("id").on_table("questions")
        table.integer("user_id").references("id").on_table("users")
        table.timestamps()

    def down(self):
        TableSchema.drop_if_exists("answers")
