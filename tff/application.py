#!flask/bin/python

import os
import datetime as dt

from flask import Flask, request, render_template
from tff.flaskrun import flaskrun
from flaskext.markdown import Markdown

from tff.db import db
from tff.database import init_db
from tff.model import Article, FeaturedArticle, Tag


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(application)
init_db(application)

Markdown(application)


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
    content_path = os.path.join('articles', article.file_path)
    context = {'article': article}
    
    if 'notebook' in (tag.name.lower() for tag in article.tags):
        context['notebook_path'] = content_path
    else:
        fullpath = os.path.join(application.static_folder, content_path)
        with open(fullpath) as f:
            content = f.read()
            
            if content_path[-3:].lower() == '.md':
                context['markdown_content'] = content
            else:
                context['html_content'] = content

    return render_template('article.html', **context)


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


if __name__ == '__main__':
    flaskrun(application)
