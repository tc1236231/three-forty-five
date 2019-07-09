from flask import Blueprint, render_template, jsonify
from google.cloud import bigquery

blueprint = Blueprint('chart', __name__)


@blueprint.route('/chart')
def index():
    return render_template(
        'chart.html'
    )


@blueprint.route('/attendance')
def attendance():
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `mnhs-dw-prod.dw.visits_monthly_full_padded_view` '
         )

    try:
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
        total = []
        for row in rows:
            data = {}
            data['site'] = row.site_name
            data['category'] = row.category_name
            data['count'] = row.count
            data['month'] = row.month
            data['year'] = row.year
            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500
