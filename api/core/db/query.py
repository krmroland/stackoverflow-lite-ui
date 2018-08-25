from flask import abort
from . import Connect


class DB:
    def __init__(self, table_name):
        self.table_name = table_name
        self._wheres = None
        self._where_bindings = []
        self._columns = None
        self.connection = Connect.connect()
        self.cursor = self.connection.cursor()

    def table_columns(self):
        if not self._columns:
            self.cursor.execute(
                "select column_name from information_schema.columns\
                 where  table_name = %s",
                [self.table_name]
            )
            columns = self._fetch_all()

            self._columns = [column[0] for column in columns]

        return self._columns

    @classmethod
    def table(cls, table):
        return DB(table)

    def base_where(self, query_type, args, kwargs):
        if (len(args) == 1):
            filters = args[0]
        else:
            filters = kwargs

        if not filters:
            return self

        self._wheres = "WHERE {}".format(
            f" {query_type} ".join([f"{key}=%s" for key in filters])
        )
        self._where_bindings = list(filters.values())
        return self

    def where(self, *args, **kwargs):
        return self.base_where("and", args, kwargs)

    def or_where(self, *args, **kwargs):
        return self.base_where("or", args, kwargs)

    def get(self):
        sql = f"SELECT * from {self.table_name}  {self._wheres}"

        try:
            self.cursor.execute(sql, self._where_bindings)
            return self._dictify_all()
        except Exception as e:
            self.connection.rollback()
            raise e

    def insert(self, data):
        columns = ",".join([key for key in data])
        holders = ",".join(["%s" for key in data])
        sql = f"INSERT into {self.table_name} ({columns}) VALUES({holders})"
        try:
            self.cursor.execute(sql, list(data.values()))
            self.cursor.execute('SELECT LASTVAL()')
            id = self._fetch_one()
            data["id"] = id[0]
            self.connection.commit()
            return data
        except Exception as e:
            self.connection.rollback()
            raise e

    def delete(self):
        if not self._where_bindings:
            return False
        sql = f"DELETE  from {self.table_name}  {self._wheres}"

        try:
            self.cursor.execute(sql, self._where_bindings)
            return self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def update(self, data):
        if not self._where_bindings:
            return False
        holders = ",".join([f"{key}= %s" for key in data])

        sql = f"UPDATE  {self.table_name} set {holders}  {self._wheres}"
        try:
            self.cursor.execute(
                sql,
                list(data.values()) + self._where_bindings
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        return data

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
        return self._dictify_all()

    def _dictify_all(self):
        try:
            results = self._fetch_all()
            return [self._dictify(result) for result in results]
        except Exception as e:
            self.connection.rollback()
            raise e

    def find(self, id):
        sql = f"Select * from {self.table_name} where id=%s"
        self.cursor.execute(sql, [id])
        return self._dictify(self._fetch_one())

    def first(self):
        sql = f"SELECT * from {self.table_name} {self._wheres}"
        self.cursor.execute(sql, self._where_bindings)
        return self._dictify(self._fetch_one())

    def first_or_fail(self):
        return self._result_or_fail(self.first())

    def find_or_fail(self, id):
        return self._result_or_fail(self.find(id))

    @classmethod
    def _result_or_fail(cls, result):
        if result:
            return result
        return abort(404)

    def _dictify(self, result):
        if not result:
            return None
        return dict(zip(self.table_columns(), result))
