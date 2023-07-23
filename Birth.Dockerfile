FROM python:3.9-slim-buster

WORKDIR /usr/app

RUN apt-get update && apt-get install -y wget

COPY ./requirements.txt /usr/app
COPY ./birth_fetch.py /usr/app
COPY ./helper.py /usr/app
COPY ./config.py /usr/app

RUN pip install --no-cache-dir -r ./requirements.txt

CMD [ "python", "./birth_fetch.py" ]