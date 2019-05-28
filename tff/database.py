import datetime as dt

from tff.db import db
from tff.model import Article, FeaturedArticle, Tag


def get_tag(name):
    return Tag.query.filter_by(name=name).one()


def add_tags():
    db.session.add_all([
        Tag(name='Dashboard'),
        Tag(name='Notebook'),
        Tag(name='HIL'),
        Tag(name='Sales'),
        Tag(name='Membership'),
        Tag(name='MHC'),
        Tag(name='Attendance'),
    ])

    db.session.commit()


def add_articles():
    db.session.add_all([
        FeaturedArticle(
            slug='attendance-yoy',
            title='Year-Over-Year Attendance Dashboard',
            date=dt.date(2019, 5, 28),
            description='Compare attendance totals to past years.',
            file_path='chart_yoy.html',
            img='img/analysis-increase-graph-statistic-512.png',
            tags=[
                get_tag('Dashboard'),
                get_tag('Attendance'),
            ]
        ),
        FeaturedArticle(
            slug='attendance',
            title='Attendance Dashboard',
            date=dt.date(2019, 3, 20),
            description='See attendance trends by site and category.',
            file_path='chart.html',
            img='img/analysis-increase-graph-statistic-512.png',
            tags=[
                get_tag('Dashboard'),
                get_tag('Attendance'),
            ]
        ),
        Article(
            slug='exhibit-att-analysis',
            title='Temporary Exhibits and History Center Attendance',
            date=dt.date(2019, 3, 19),
            description='Do temporary exhibits have any effect on History Center attendance?',
            file_path='exhibit_att_analysis.html',
            tags=[
                get_tag('Notebook'),
                get_tag('Attendance'),
                get_tag('MHC'),
            ]
        ),
        Article(
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
