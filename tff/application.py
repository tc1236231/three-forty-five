#!flask/bin/python

from flask import Flask, render_template
from tff.flaskrun import flaskrun
from flaskext.markdown import Markdown
from tff.exceptions import InvalidUsage

from tff.db import db
from tff.database import init_db
from tff import blog, chart

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(application)
init_db(application)

Markdown(application)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blog.blueprint)
    app.register_blueprint(chart.blueprint)


register_blueprints(application)


def register_errorhandlers(app):

    def errorhandler(error):
        return render_template("error.html", message=error.message, status_code=error.status_code)

    app.errorhandler(InvalidUsage)(errorhandler)


register_errorhandlers(application)


if __name__ == '__main__':
    flaskrun(application)
