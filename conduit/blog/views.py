from flask import Blueprint, render_template, flash
from conduit.articles.views import get_tags, get_article, get_articles
from conduit.exceptions import InvalidUsage
from babel.dates import format_datetime
from dateutil import parser

blueprint = Blueprint('blog', __name__)


def render_blog(uri, **kwargs):
    tags = get_tags(True, 10)
    return render_template(uri, tagsJson=tags.json['tags'], **kwargs)


'''Objects that has duplicates will be striped totally'''
def unique_json(json, key):
    result = list()
    items_set = set()
    for js in json:
        if not js[key] in items_set:
            items_set.add(js[key])
            result.append(js)
        else:
            result.remove(js)
    return result


@blueprint.route('/')
def index():
    featured_articles_response = get_articles(featured=True, latest=True, limit=2)
    latest_articles_response = get_articles(latest=True, limit=4)
    print(latest_articles_response.json)
    if featured_articles_response.status_code == 200 and latest_articles_response.status_code == 200:
        featured_articles_json = featured_articles_response.json['articles']
        latest_articles_json = unique_json(latest_articles_response.json['articles'] + featured_articles_json, 'slug')
        print(latest_articles_json)
        return render_blog('blog/index.html', featured_articles_json=featured_articles_json, latest_articles_json=latest_articles_json)
    else:
        raise InvalidUsage('Failed to retrieve articles', status_code=featured_articles_response.status_code)


@blueprint.route('/blog/article/<slug>')
def view_article(slug):
    article = get_article(slug)
    if article.status_code == 200:
        articleJson = article.json['article']
        if articleJson['filePath'] == "":
            return render_blog('blog/article.html', articleJson=articleJson)
        else:
            return render_blog('blog/static_article.html', articleJson=articleJson)
    else:
        raise InvalidUsage('Failed to get article information', status_code=article.status_code)


@blueprint.route('/blog/tag/<name>')
def view_tags(name):
    return render_template('blog/tag.html')


@blueprint.add_app_template_filter
def datetime(value, format='medium'):
    datetime_obj = parser.parse(value)
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="MMMM d, y"
    return format_datetime(datetime_obj, format, locale="en_US")

