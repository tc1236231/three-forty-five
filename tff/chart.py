from flask import Blueprint, render_template, jsonify, Response
from google.cloud import bigquery

blueprint = Blueprint('chart', __name__)

project_name = 'mnhs-dw-prod'
query_tables = {
    'yearly': '{}.dw.visits_yearly_full_padded_view'.format(project_name),
    'quarterly': '{}.dw.visits_quarterly_full_padded_view'.format(project_name),
    'monthly': '{}.dw.visits_monthly_full_padded_view'.format(project_name),
    'weekly': '{}.dw.visits_weekly_full_padded_view'.format(project_name),
    'daily': '{}.dw.visits_daily_full_padded_view'.format(project_name),
}


@blueprint.route('/api/attendance/data/<string:mode>')
def attendance(mode):
    client = bigquery.Client()

    query_table = query_tables[mode]

    QUERY = (
        'SELECT * FROM `{}` '.format(query_table)
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
            if(mode == "yearly"):
                data['date'] = row.year_start
            if (mode == "quarterly"):
                data['date'] = row.quarter_start
            if (mode == "monthly"):
                data['date'] = row.month_start
            if (mode == "weekly"):
                data['date'] = row.week_start
            if (mode == "daily"):
                data['date'] = row.date
            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500

