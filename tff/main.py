#!flask/bin/python

from flask import Flask, render_template
from tff.flaskrun import flaskrun
from flaskext.markdown import Markdown
from tff.exceptions import InvalidUsage

from tff.db import db
from tff.database import init_db
from tff import blog, chart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

Markdown(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blog.blueprint)
    app.register_blueprint(chart.blueprint)


register_blueprints(app)


def register_errorhandlers(app):

    def errorhandler(error):
        return render_template("error.html", message=error.message, status_code=error.status_code)

    app.errorhandler(InvalidUsage)(errorhandler)


register_errorhandlers(app)


if __name__ == '__main__':
    flaskrun(app)
