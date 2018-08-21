FROM python:3.6

WORKDIR /app

COPY ./src requirements.txt ./

RUN pip install -r requirements.txt

CMD python server.py