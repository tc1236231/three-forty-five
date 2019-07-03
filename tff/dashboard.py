from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('dashboard', __name__)


@blueprint.route('/dashboard')
def index():
    return render_template(
        '/dashboard/chart.html'
    )

@blueprint.route('/dashboard/yoy')
def yoy():
    return render_template(
        '/dashboard/chart_yoy.html'
    )