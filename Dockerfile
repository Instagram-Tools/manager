FROM python:3.6.6-alpine3.8

WORKDIR /app

COPY ./src requirements.txt ./

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=0
CMD python start.py