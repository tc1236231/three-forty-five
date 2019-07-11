from flask import Blueprint, render_template, jsonify
from google.cloud import bigquery

blueprint = Blueprint('chart', __name__)


@blueprint.route('/chart')
def index():
    return render_template(
        'chart.html'
    )


@blueprint.route('/api/attendance/monthly')
def attendance_monthly():
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `mnhs-dw-test.dw.visits_monthly_full_padded_view` '
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


@blueprint.route('/api/attendance/daily')
def attendance_daily():
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `mnhs-dw-test.dw.visits_daily_full_padded_view` '
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
            data['date'] = row.date
            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500


@blueprint.route('/api/attendance/weekly')
def attendance_weekly():
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `mnhs-dw-test.dw.visits_weekly_full_padded_view` '
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
            data['date'] = row.wk
            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500


@blueprint.route('/api/attendance/quarterly')
def attendance_quarterly():
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `mnhs-dw-test.dw.visits_quarterly_full_padded_view` '
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
            data['date'] = row.date
            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500


@blueprint.route('/api/attendance/yearly')
def attendance_yearly():
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `mnhs-dw-test.dw.visits_yearly_full_padded_view` '
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
            data['date'] = row.year
            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500