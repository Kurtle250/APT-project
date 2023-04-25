# NOTE: this example is taken from the default Dockerfile for the official nginx Docker Hub Repo
# https://hub.docker.com/_/nginx/
# NOTE: This file is slightly different than the video, because nginx versions have been updated
#       to match the latest standards from docker hub... but it's doing the same thing as the video
#       describes

# import docker image from docker hub of python latest
FROM python:latest

LABEL authors="kurt"

# optional environment variable that's used in later lines and set as envvar when container is running
#ENV PYTHON_Version 23.2

WORKDIR /usr/src/APT_app

COPY .. .

COPY .. /usr/src/APT_app

RUN pip install -r requirements.txt

CMD bash