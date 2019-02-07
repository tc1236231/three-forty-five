import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db():
    if db is None:
        raise RuntimeError("The database instance has not been initialized!")

    return db

def init_db():
    get_db().create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized database schema.')

def init_app(app):
    app.cli.add_command(init_db_command)
    db.init_app(app)
