from api.core.db.Migration import Migration, TableSchema


class UsersTable(Migration):

    def up(self):
        table = TableSchema.create("users")
        table.increments("id")
        table.string("email", 150)
        table.string("name", 150)
        table.string("password", 125)
        table.timestamps()

    def down(self):
        TableSchema.drop_if_exists("users")
