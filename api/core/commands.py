import click
from flask.cli import AppGroup, with_appcontext
from api.core.db.Migration import Migration
from api.core.db import Connect
from api.app.databases.migrations import migrations


def migrate():
    conn = Connect.connect()
    cur = conn.cursor()
    for migration in migrations:
        migration._run_down()
        migration._run_up()
    queries = Migration.get_all_tables_sql()

    for sql in queries:
        cur.execute(sql)
        conn.commit()
    conn.close()


db_cli = AppGroup('db')


@db_cli.command('migrate:fresh', short_help='Drops and recreates all tables')
@with_appcontext
def migrate_command():
    click.echo("Running migrations")
    migrate()
    click.echo("Finished Running migrations")
