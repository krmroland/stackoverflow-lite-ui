import psycopg2
from flask import current_app


class Connect:
    @classmethod
    def connect(cls):
        return psycopg2.connect(f"dbname={current_app.config.get('DB_NAME')}")


__all__ = ["Connect"]
