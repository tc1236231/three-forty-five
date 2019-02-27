import datetime as dt

import pytest

from tff.application import application
from tff.db import db
from tff.model import Article


@pytest.fixture
def app():
    db.drop_all(app=application)
    db.create_all(app=application)
    
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    assert client.get('/').status_code == 200


def test_articles(client):
    assert client.get('/articles').status_code == 200

    
def test_article(app, client):
    with app.app_context():
        db.session.add(Article(
            slug='an-article',
            title='An Article',
            date=dt.date(2018, 3, 14),
            description='Definitely just an article.',
            file_path='hil_analysis.html',
            tags=[
            ]
        ))

    client.get('/article/an-article').status_code == 200

