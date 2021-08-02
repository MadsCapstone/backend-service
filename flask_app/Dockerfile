FROM python:3.8-slim
MAINTAINER Ermias Bizuwork "ebizuwork@gmail.com"
COPY ./ /flask_app
WORKDIR /flask_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install .
RUN gunicorn -w 1 -b 0.0.0.0:8000 wsgi:app