import datetime as dt

from tff.db import db
from tff.model import Article, FeaturedArticle, Tag


def get_tag(name):
    return Tag.query.filter_by(name=name).one()


def add_tags():
    db.session.add_all([
        Tag(name='Notebook'),
        Tag(name='HIL'),
        Tag(name='Sales'),
        Tag(name='Membership'),
    ])

    db.session.commit()


def add_articles():
    db.session.add_all([
        FeaturedArticle(
            slug='mbr-att-ren-analysis.html',
            title='Member Renewal and Attendance Analysis',
            date=dt.date(2019, 3, 15),
            description='Is a member more likely to renew their membership if they have visited a site?',
            file_path='mbr_att_and_ren_analysis.html',
            tags=[
                get_tag('Notebook'),
                get_tag('Membership'),
            ]
        ),
        Article(
            slug='hil_analysis',
            title='Hill House Ticket Sales Analysis',
            date=dt.date(2019, 1, 1),
            description='Interventions begun in the holiday season of FY18 resulted in more than $40,000 of additional sales over the previous year.',
            file_path='hil_analysis.html',
            tags=[
                get_tag('Notebook'),
                get_tag('HIL'),
                get_tag('Sales'),
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
