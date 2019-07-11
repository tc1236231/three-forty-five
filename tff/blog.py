import os
import datetime as dt

from flask import Blueprint, request, render_template, current_app

from tff.exceptions import InvalidUsage
from tff.model import Article, FeaturedArticle, Tag, article_tag
from flask_sqlalchemy import sqlalchemy

blueprint = Blueprint('blog', __name__, url_prefix='/deprecated')


@blueprint.route('/blog')
def index():
    return render_template(
        'index.html',
        tags=Tag.query.all(),
        featured_articles=FeaturedArticle.query.all(),
        latest_articles=Article.query.order_by(Article.date.desc()).limit(5)
    )


@blueprint.route('/article/<slug>')
def article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    content_path = os.path.join('articles', article.file_path)
    context = {'article': article}

    tags = [tag.name.lower() for tag in article.tags]
    if 'notebook' in tags:
        context['notebook_path'] = content_path
    elif 'dashboard' in tags:
        context['dashboard_template'] = os.path.join('dashboards',
                                                     article.file_path)
    else:
        fullpath = os.path.join(current_app.static_folder, content_path)
        with open(fullpath) as f:
            content = f.read()

            if content_path[-3:].lower() == '.md':
                context['markdown_content'] = content
            else:
                context['html_content'] = content

    return render_template('article.html', **context)


@blueprint.route('/articles')
def articles():
    tag_name = request.args.get('tag_name')

    if tag_name:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            raise InvalidUsage.tag_not_found()
        articles = tag.articles
    else:
        articles = Article.query.all()

    return render_template('articles.html',
                           tags=Tag.query.all(),
                           articles=articles,
                           selected_tag=tag_name)


@blueprint.route('/search')
def search():
    input = request.args.get('txt')
    if not input:
        return render_template('search.html')
    else:
        articles = Article.query.filter(
            (Article.title.like('%' + input + '%')) |
            (Article.description.like('%' + input + '%')) |
            (Article.tags.any(name=input))
        )
        return render_template('search.html', txt=input, articles=articles)


@blueprint.add_app_template_filter
def datetime(value):
    date_obj = dt.date.fromisoformat(str(value))
    return date_obj.strftime("%B %d, %Y")


@blueprint.add_app_template_global
def top_tags():
    result = (Tag.query
              .join(article_tag)
              .group_by(Tag.id)
              .order_by(sqlalchemy.func.count('*'))
              .limit(10)
              .all())
    return result
