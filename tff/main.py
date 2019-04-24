#!flask/bin/python
import os

from flask import Flask, render_template, redirect, url_for, request
from flask_dance.contrib.google import make_google_blueprint, google

from tff.flaskrun import flaskrun
from flaskext.markdown import Markdown
from tff.exceptions import InvalidUsage

from tff.db import db
from tff.database import init_db
from tff import blog, chart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # This should be removed once we have HTTPS
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "mnhssecretkey")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
google_bp = make_google_blueprint()

db.init_app(app)
init_db(app)

Markdown(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blog.blueprint)
    app.register_blueprint(chart.blueprint)
    app.register_blueprint(google_bp)


register_blueprints(app)


def register_errorhandlers(app):

    def errorhandler(error):
        return render_template("error.html", message=error.message, status_code=error.status_code)

    app.errorhandler(InvalidUsage)(errorhandler)


register_errorhandlers(app)


@app.before_request
def before_request():
    if not google.authorized and (request.endpoint != 'google.login' and request.endpoint != 'google.authorized'):
        return redirect(url_for('google.login'))

    if request.endpoint != 'google.login' and request.endpoint != 'google.authorized':
        try:
            resp = google.get("/oauth2/v1/userinfo")
            assert resp.ok, resp.text
        except:
            return redirect(url_for('google.login'))


if __name__ == '__main__':
    flaskrun(app)
