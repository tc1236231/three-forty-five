FROM tiangolo/uwsgi-nginx-flask:python3.7

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV STATIC_PATH /app/tff/static