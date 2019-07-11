from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('dashboard', __name__)


@blueprint.route('/')
def index():
    return render_template(
        '/dashboard/chart.html'
    )


@blueprint.route('/dashboard/daily')
def daily():
    return render_template(
        '/dashboard/chart_daily.html'
    )


@blueprint.route('/dashboard/weekly')
def weekly():
    return render_template(
        '/dashboard/chart_weekly.html'
    )

@blueprint.route('/dashboard/quarterly')
def quarterly():
    return render_template(
        '/dashboard/chart_quarterly.html'
    )

@blueprint.route('/dashboard/yearly')
def yearly():
    return render_template(
        '/dashboard/chart_yearly.html'
    )

@blueprint.route('/dashboard/yoy')
def yoy():
    return render_template(
        '/dashboard/chart_yoy.html'
    )