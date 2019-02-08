from flask import Blueprint, render_template

blueprint = Blueprint('blog', __name__)

@blueprint.route('/')
def index():
    return render_template('blog/index.html')
