FROM python:3.11-buster

WORKDIR /zooworld

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt install -y python3-dev &&\
    apt-get install -y postgresql

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .