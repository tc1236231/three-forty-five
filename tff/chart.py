import os

from flask import Blueprint, render_template, jsonify, Response
from google.cloud import bigquery

from tff.db import cache

blueprint = Blueprint('chart', __name__)

project_name = os.getenv('DW_PROJECT_ID')
query_tables = {
    'hourly_heat': '{}.dw.visits_hourly_heat_full_padded_view'.format(project_name),
    'hourly': '{}.dw.visits_hourly_full_padded_view_new'.format(project_name),
    'yearly': '{}.dw.visits_yearly_view'.format(project_name),
    'quarterly': '{}.dw.visits_quarterly_view'.format(project_name),
    'monthly': '{}.dw.visits_monthly_view'.format(project_name),
    'weekly': '{}.dw.visits_weekly_view'.format(project_name),
    'daily': '{}.dw.visits_daily_view'.format(project_name),
}


@blueprint.route('/api/attendance/data/<string:mode>')
@cache.cached(timeout=600)
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
            data['count'] = row.count
            if mode == "yearly":
                data['date'] = row.year_start
                data['category'] = row.category_name
            if mode == "quarterly":
                data['date'] = row.quarter_start
                data['category'] = row.category_name
            if mode == "monthly":
                data['date'] = row.month_start
                data['category'] = row.category_name
            if mode == "weekly":
                data['date'] = row.week_start
                data['category'] = row.category_name
            if mode == "daily":
                data['date'] = row.date
                data['category'] = row.category_name
            if mode == "hourly":
                data['year'] = row.year
                data['dayofweek'] = row.dayofweek
                data['hour'] = row.hour
                data['category'] = row.category_name
            if mode == "hourly_heat":
                data['year'] = row.year
                data['month'] = row.month
                data['day'] = row.day
                data['hour'] = row.hour

            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500


@blueprint.route('/api/revenue/data/<string:mode>')
@cache.cached(timeout=600)
def revenue(mode):
    client = bigquery.Client()

    query_table = '{}.dw.shopify_daily_revenue_view'.format(project_name)

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
            data['date'] = row.date
            data['revenue'] = row.revenue

            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500
