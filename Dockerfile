FROM python:latest
# Check tag here: https://hub.docker.com/_/python

MAINTAINER vuhi, kmuni08

ENV PYTHONUNBUFFERED=1

# make "slack_clone_api" directory inside docker container & set it as a default location
# which mean: / == /slack_clone_api
RUN mkdir /slack_clone_api

# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR /slack_clone_api

# use this cmd to generate requirements.txt first: "pip freeze > requirements.txt"
# requirements.txt ~ package.json
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy rest of the file & ignore any in .dockerignore
COPY . /slack_clone_api


