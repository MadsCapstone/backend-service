FROM tiangolo/uwsgi-nginx-flask:python3.8
MAINTAINER Ermias Bizuwork "ebizuwork@gmail.com"
WORKDIR /backend-api
COPY src /app

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
