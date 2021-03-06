FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN python setup.py develop
