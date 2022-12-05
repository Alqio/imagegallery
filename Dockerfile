FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y python3-pip

RUN ln /usr/bin/python3 /usr/bin/python
RUN ln /usr/bin/pip3 /usr/bin/pip

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# RUN python manage.py migrate

ENTRYPOINT ["python", "manage.py", "runserver"]
