from api.core.Utils import Fluent


class DataTypeCompiler:
    def __init__(self, DataType):
        self.attributes = DataType.attributes

    def compile(self):
        self.compiled = [self.attributes.name, self.type()]
        self.compile_attributes()

        return " ".join(self.compiled)

    def type(self):
        type = self.attributes.type
        if type == "string":
            return f"VARCHAR ({self.attributes.length})"
        if type == "timestamp":
            return "timestamp without time zone"
        if type == "serial":
            return "SERIAL PRIMARY KEY"
        return type.upper()

    def compile_attributes(self):

        if self.attributes.nullable:
            self.compiled.append("NULL")
        elif not self.attributes.type == "serial":
            self.compiled.append("NOT NULL")

        if self.attributes.references:
            self.compiled.append(
                "REFERENCES {}({})".format(
                    self.attributes.on_table,
                    self.attributes.references
                )
            )


class DataType:
    def __init__(self, name, length=None):
        self.attributes = Fluent(
            dict(
                type=type,
                name=name,
                length=length,
                nullable=False,
                is_primary=False
            )
        )

    def compile(self):
        return DataTypeCompiler(self).compile()

    def __getattr__(self, key):
        def _method(value=True):
            self.attributes[key] = value
            return self
        return _method


class TableSchema:
    _global_commands = []
    _defined_tables = []

    def __init__(self, table_name):
        self.table_name = table_name
        self.fields = []
        self.commands = []
        self._defined_tables.append(self)

    @classmethod
    def create(cls, table_name):
        return cls(table_name)

    def add_field(self, field):
        self.fields.append(field)
        return field

    def integer(self, name, length=None):
        return self.add_field(DataType(name, length).type("integer"))

    def string(self, name, length=250):
        return self.add_field(DataType(name, length).type("string"))

    def text(self, name, length=250):
        return self.add_field(DataType(name, length).type("text"))

    def timestamps(self):
        self.timetsamp("created_at").nullable()
        self.timetsamp("updated_at").nullable()

    def timetsamp(self, name):
        return self.add_field(DataType(name).type("timestamp"))

    def increments(self, name):
        return self.add_field(DataType(name).type("serial"))

    @classmethod
    def drop_if_exists(cls, table):
        return cls.add_global_command(f"drop table if exists {table} cascade")

    @classmethod
    def add_global_command(cls, command):
        cls._global_commands.append(command)

    def compile_sql(self):
        values = ",".join([field.compile() for field in self.fields])
        self.add_global_command(f"create table {self.table_name} ({values}) ")


class Migration:
    _defined_migrations = []
    _compiled_sql = None

    def __init__(self):
        self._defined_migrations.append(self)
        self._has_run_down = False
        self._has_run_up = False

    def up(self):
        raise NotImplementedError()

    def down(self):
        raise NotImplementedError()

    def _run_down(self):
        if self._has_run_down:
            return
        self.down()
        self._has_run_down = True

    def _run_up(self):
        if self._has_run_up:
            return
        self.up()
        self._has_run_up = True

    @classmethod
    def defined_migrations(cls):
        return cls._defined_migrations

    @classmethod
    def get_all_tables_sql(cls):
        if not cls._compiled_sql:
            for Table in TableSchema._defined_tables:
                Table.compile_sql()
            cls._compiled_sql = TableSchema._global_commands
        return cls._compiled_sql
