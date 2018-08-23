import psycopg2


class Connect:
    @classmethod
    def connect(cls):
        return psycopg2.connect("dbname=stackoverflow")


__all__ = ["Connect"]
