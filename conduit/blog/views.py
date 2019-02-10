from flask import Blueprint, render_template, flash
from conduit.articles.views import get_tags

blueprint = Blueprint('blog', __name__)

@blueprint.route('/')
def index():
    tags = get_tags(True, 10)
    return render_template('blog/index.html', tagsJson=tags.json)
