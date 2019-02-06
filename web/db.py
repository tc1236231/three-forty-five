import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_db():
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized database schema.')


def init_app(app):
    app.cli.add_command(init_db_command)
    db.init_app(app)
