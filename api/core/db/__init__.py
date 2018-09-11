from os import getenv
import psycopg2
from flask import current_app


class Connect:
    @classmethod
    def connect(cls):
        if getenv("FLASK_ENV") == "production":
            dsn = getenv("DATABASE_URL")
        else:
            dsn = f"dbname={current_app.config.get('DB_NAME')}"
        return psycopg2.connect(dsn)


__all__ = ["Connect"]
