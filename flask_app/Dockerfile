FROM python:3.8-slim
MAINTAINER Ermias Bizuwork "ebizuwork@gmail.com"
COPY ./ /flask_app
WORKDIR /flask_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install .

