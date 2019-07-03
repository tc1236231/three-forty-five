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
    url = "https://34.66.87.38/attendance"
    try:
        res = requests.get(url, verify=False)
        return jsonify(res.json())
    except:
        return jsonify('something went wrong'), 500
