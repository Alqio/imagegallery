FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8

RUN apt-get update

RUN apt-get install -y python3-pip

RUN ln /usr/bin/python3 /usr/bin/python
RUN ln /usr/bin/pip3 /usr/bin/pip

WORKDIR /app

# Copy only requirements.txt to avoid needing to rebuild if a project file is changed
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
