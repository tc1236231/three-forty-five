import datetime as dt

from tff.db import db
from tff.model import Article, FeaturedArticle, Tag


def get_tag(name):
    return Tag.query.filter_by(name=name).one()


def add_tags():
    db.session.add_all([
        Tag(name='Notebook'),
        Tag(name='Cool'),
        Tag(name='Hip'),
        Tag(name='Easy'),
        Tag(name='Free'),
    ])

    db.session.commit()


def add_articles():
    db.session.add_all([
        FeaturedArticle(
            slug='an-article',
            title='An Article',
            date=dt.datetime.utcnow(),
            description='Definitely just an article.',
            file_path='hil_analysis.html',
            tags=[
                get_tag('Notebook'),
                get_tag('Hip'),
                get_tag('Cool'),
            ]
        ),
        Article(
            slug='another-article',
            title='Another Article',
            date=dt.datetime.utcnow(),
            description='Yep... Here is another one.',
            file_path='another-article.html',
            tags=[
                get_tag('Free'),
                get_tag('Easy'),
                get_tag('Cool'),
            ]
        ),
        FeaturedArticle(
            slug='yet-another-article',
            title='Yet Another Article',
            date=dt.datetime.utcnow(),
            description='Just so many articles.',
            file_path='yet-another-article.md',
            tags=[
                get_tag('Easy'),
            ]
        )
    ])

    db.session.commit()


def init_db(app):
    with app.app_context():
        db.create_all(app=app)

        add_tags()
        add_articles()

        db.session.commit()
