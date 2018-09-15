from api.core.exceptions import ModelNotFoundException
from . import Connect


class DB:
    def __init__(self, table_name):
        self.table_name = table_name
        self._wheres = None
        self._where_bindings = []
        self._columns = None
        self.connection = Connect.connect()
        self.cursor = self.connection.cursor()

    @classmethod
    def table(cls, table):
        return DB(table)

    def base_where(self, query_type, args, kwargs):
        if (len(args) == 1):
            filters = args[0]
        else:
            filters = kwargs

        if not filters:
            return self  # pragma: no cover

        self._wheres = "WHERE {}".format(
            f" {query_type} ".join([f"{key}=%s" for key in filters])
        )
        self._where_bindings = list(filters.values())
        return self

    def where_in(self, column_name, values):
        place_holders = ",".join(["%s"] * len(values))
        self._wheres = f"WHERE {column_name} in ({place_holders})"
        self._where_bindings = values
        return self

    def where(self, *args, **kwargs):
        return self.base_where("and", args, kwargs)

    def or_where(self, *args, **kwargs):
        return self.base_where("or", args, kwargs)

    def get(self, fields=None):
        if fields:
            fields = ",".join([field for field in fields])
        else:
            fields = "*"

        sql = f"SELECT {fields} from {self.table_name}  {self._wheres}"

        try:
            self.cursor.execute(sql, self._where_bindings)
            return self._fetch_all()
        except Exception as e:
            self.connection.rollback()
            raise e

    def insert(self, data):
        columns = ",".join([key for key in data])
        holders = ",".join(["%s" for key in data])
        sql = "INSERT into {} ({}) VALUES({}) RETURNING *".format(
            self.table_name, columns, holders
        )
        try:
            self.cursor.execute(sql, list(data.values()))
            self.connection.commit()
            return self._fetch_one()
        except Exception as e:
            self.connection.rollback()
            raise e

    def exists(self):
        if not self._wheres:
            return False  # pragma: no cover
        sql = f"SELECT exists (SELECT * from {self.table_name} {self._wheres})"
        try:
            self.cursor.execute(sql, self._where_bindings)
            return self._fetch_one()["exists"]
        except Exception as e:
            self.connection.rollback()
            raise e

    def delete(self):
        if not self._where_bindings:
            return False  # pragma: no cover
        sql = f"DELETE  from {self.table_name}  {self._wheres}"

        try:
            self.cursor.execute(sql, self._where_bindings)
            return self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def update(self, data):
        if not self._where_bindings:
            return False  # pragma: no cover
        holders = ",".join([f"{key}= %s" for key in data])

        sql = "UPDATE  {} set {}  {} RETURNING *".format(
            self.table_name, holders, self._wheres
        )
        try:
            self.cursor.execute(
                sql,
                list(data.values()) + self._where_bindings
            )
            self.connection.commit()
            return self._fetch_one()
        except Exception as e:
            self.connection.rollback()
            raise e

    def order_by(self):
        pass

    def _fetch_one(self):
        try:
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()
            raise e

    def _fetch_all(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e

    def all(self):
        self.cursor.execute(f"SELECT * from {self.table_name}")
        return self._fetch_all()

    def find(self, id):
        sql = f"Select * from {self.table_name} where id=%s"
        self.cursor.execute(sql, [id])
        return self._fetch_one()

    def first(self):
        sql = f"SELECT * from {self.table_name} {self._wheres}"
        self.cursor.execute(sql, self._where_bindings)
        return self._fetch_one()

    def first_or_fail(self):
        return self._result_or_fail(self.first())

    def find_or_fail(self, id):
        return self._result_or_fail(self.find(id))

    @classmethod
    def _result_or_fail(cls, result):
        if result:
            return result
        raise ModelNotFoundException()
