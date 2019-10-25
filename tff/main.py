#!flask/bin/python
import os

from flask import Flask, render_template

from tff.flaskrun import flaskrun
from flaskext.markdown import Markdown
from tff.exceptions import InvalidUsage

from tff.db import db, cache
from tff.database import init_db
from tff import blog, chart, dashboard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "mnhssecretkey")

db.init_app(app)
cache.init_app(app)
init_db(app)

Markdown(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blog.blueprint)
    app.register_blueprint(chart.blueprint)
    app.register_blueprint(dashboard.blueprint)


register_blueprints(app)


def register_errorhandlers(app):

    def errorhandler(error):
        return render_template(
            "error.html", message=error.message, status_code=error.status_code)

    app.errorhandler(InvalidUsage)(errorhandler)


register_errorhandlers(app)


@app.template_filter()
def env_override(value, key):
    return os.getenv(key, value)


if __name__ == '__main__':
    flaskrun(app)
