import click
from flask.cli import AppGroup
from api.core.db.Migration import Migration
from api.core.db import Connect
from api.app.databases.migrations import migrations

db_cli = AppGroup('db')


@db_cli.command('migrate', short_help='runs a fresh migration of all tables ')
def migrate_command():

    for migration in migrations:
        migration.down()
        migration.up()
    queries = Migration.get_all_tables_sql()
    click.echo("Running migrations")
    conn = Connect.connect()
    cur = conn.cursor()
    for sql in queries:
        cur.execute(sql)
    conn.commit()
    click.echo("Finished Running migrations")
    conn.close()
