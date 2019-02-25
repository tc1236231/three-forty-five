#!flask/bin/python
from flask import Flask
from tff.flaskrun import flaskrun
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
admin = User(username='admin', email='admin@example.com')
db.session.add(admin)
db.session.commit()


@application.route('/')
def index():
    return "Hello {}".format(User.query.filter_by(username='admin').first().username)


if __name__ == '__main__':
    flaskrun(application)
