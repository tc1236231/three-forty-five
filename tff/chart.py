import os

from flask import Blueprint, render_template, jsonify, Response
from google.cloud import bigquery

from tff.db import cache

blueprint = Blueprint('chart', __name__)

project_name = os.getenv('DW_PROJECT_ID')
query_tables = {
    'hourly_heat': '{}.tff.attendance_hourly_heat_map_view'.format(project_name),
    'hourly_holiday': '{}.tff.attendance_hourly_holidays_view'.format(project_name),
    'hourly': '{}.tff.attendance_hourly_view'.format(project_name),
    'yearly': '{}.tff.attendance_yearly_view'.format(project_name),
    'quarterly': '{}.tff.attendance_quarterly_view'.format(project_name),
    'monthly': '{}.tff.attendance_monthly_view'.format(project_name),
    'weekly': '{}.tff.attendance_weekly_view'.format(project_name),
    'daily': '{}.tff.attendance_daily_view'.format(project_name),
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
                data['dayofweek'] = row.wday
                data['hour'] = row.hour
                data['category'] = row.attendance_category_name
                data['total'] = row.sample_size
            if mode == "hourly_holiday":
                data['year'] = row.year
                data['holiday'] = row.holiday
                data['hour'] = row.hour
                data['category'] = row.attendance_category_name
                data['total'] = row.sample_size
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

    query_table = '{}.tff.shopify_daily_revenue_view'.format(project_name)

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


@blueprint.route('/api/nps/data/<string:mode>')
@cache.cached(timeout=600)
def nps(mode):
    client = bigquery.Client()

    query_table = '{}.tff.nps_monthly_view'.format(project_name)

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
            data['date'] = row.month_start
            data['nps'] = row.nps
            data['sample_size'] = row.sample_size

            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500


@blueprint.route('/api/weather/data/<string:mode>')
@cache.cached(timeout=600)
def weather(mode):
    client = bigquery.Client()

    query_table = '{}.tff.weather_view'.format(project_name)

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
            data['prcp'] = row.prcp
            data['snow'] = row.snow
            data['tmax'] = row.tmax
            data['tmin'] = row.tmin

            total.append(data)

        return jsonify(total)
    except Exception as e:
        return jsonify('Error: ' + str(e)), 500
