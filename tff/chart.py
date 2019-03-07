import os

from flask import Blueprint, request, render_template, current_app
from tff.exceptions import InvalidUsage
from tff.model import Article, FeaturedArticle, Tag, article_tag
from flask_sqlalchemy import sqlalchemy

blueprint = Blueprint('chart', __name__)


@blueprint.route('/chart')
def index():
    return render_template(
        'chart.html'
    )
