#!flask/bin/python

import datetime as dt

from flask import Flask, request, render_template
from tff.flaskrun import flaskrun
from flask_sqlalchemy import SQLAlchemy


# Setup ------------------------------------------------------------------------

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


# Models -----------------------------------------------------------------------

article_tag = db.Table(
    'article_tag',
    db.Column('article', db.Integer, db.ForeignKey('article.id')),
    db.Column('tag', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    articles = db.relationship('Article',
                               secondary=article_tag,
                               back_populates='tags')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    slug = db.Column(db.Text, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255))

    tags = db.relationship('Tag',
                           secondary=article_tag,
                           back_populates='articles')

    __mapper_args__ = {
        'polymorphic_identity':'article',
        'polymorphic_on': type
    }


class FeaturedArticle(Article):
    id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'featured_article',
    }


## Testing ---------------------------------------------------------------------

cool_tag = Tag(name='Cool')

db.create_all()
db.session.add_all([
    FeaturedArticle(
        slug='an-article',
        title='An Article',
        date=dt.datetime.utcnow(),
        description='Definitely just an article.',
        file_path='somewhere',
        tags=[Tag(name='Hip'), cool_tag]
    ),
    Article(
        slug='another-article',
        title='Another Article',
        date=dt.datetime.utcnow(),
        description='Yep... Here is another one.',
        file_path='somewhere_else',
        tags=[Tag(name='Free'), Tag(name='Easy'), cool_tag]
    ),
    FeaturedArticle(
        slug='yet-another-article',
        title='Yet Another Article',
        date=dt.datetime.utcnow(),
        description='Just so many articles.',
        file_path='somewhere',
        tags=[Tag(name='Sassy'), Tag(name='Naughty')]
    )
])
db.session.commit()


# Views ------------------------------------------------------------------------

@application.route('/')
def index():
    return render_template(
        'index.html',
        tags=Tag.query.all(),
        featured_articles=FeaturedArticle.query.all(),
        latest_articles=Article.query.order_by(Article.date.desc()).limit(5)
    )


@application.route('/article/<slug>')
def article(slug):
    article = Article.query.filter_by(slug=slug).one()

    return render_template('article.html', article=article)

    #         file_path = str(articleJson['filePath'])
    #         if file_path[-3:] == ".md" or file_path[-3:] == ".MD":
    #             with current_app.open_resource("../pages/static/" + file_path) as f:
    #                 content = f.read()
    #                 articleJson['body'] = markdown(content.decode("utf-8"))
    #             return render_blog('blog/article.html', articleJson=articleJson)
    #         else:
    #             return render_blog('blog/static_article.html', articleJson=articleJson)
    # else:
    #     raise InvalidUsage('Failed to get article information', status_code=article.status_code)


@application.route('/articles')
def articles():
    tag_name = request.args.get('tag_name')
    
    if tag_name:
        articles = Tag.query.filter_by(name=tag_name).first().articles
    else:
        articles = Article.query.all()
        
    return render_template('articles.html',
                           tags=Tag.query.all(),
                           articles=articles,
                           selected_tag=tag_name)


# Main -------------------------------------------------------------------------

if __name__ == '__main__':
    flaskrun(application)
