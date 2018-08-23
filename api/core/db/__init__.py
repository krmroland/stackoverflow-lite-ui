import psycopg2


class Connect:
    connection = None

    @classmethod
    def connect(cls):
        if not cls.connection:
            cls.connection = psycopg2.connect("dbname=stackoverflow")
        return cls.connection


__all__ = ["Connect"]
