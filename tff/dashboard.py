from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('dashboard', __name__)


@blueprint.route('/')
def index():
    return render_template(
        '/dashboard/chart.html'
    )


@blueprint.route('/dashboard/yoy')
def yoy():
    return render_template(
        '/dashboard/chart_yoy.html'
    )


@blueprint.route('/dashboard/hourly')
def hourly():
    return render_template(
        '/dashboard/chart_hourly.html'
    )


@blueprint.route('/dashboard/hourly_heat')
def hourly_heat():
    return render_template(
        '/dashboard/chart_hourly_heat.html'
    )


@blueprint.route('/dashboard/table_revenue')
def table_revenue():
    return render_template(
        '/dashboard/table_revenue.html'
    )
