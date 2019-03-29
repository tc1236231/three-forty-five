from flask import Blueprint, render_template, jsonify
from tff.exceptions import InvalidUsage
import requests

blueprint = Blueprint('chart', __name__)


@blueprint.route('/chart')
def index():
    return render_template(
        'chart.html'
    )


@blueprint.route('/attendance')
def attendance():
    url = "http://ec2-18-222-170-180.us-east-2.compute.amazonaws.com/monthly-attendance"
    try:
        res = requests.get(url)
        return jsonify(res.json())
    except:
        return jsonify('something went wrong'), 500
