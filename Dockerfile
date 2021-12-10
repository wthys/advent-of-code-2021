FROM python:3.10

WORKDIR /app

COPY requirements.txt *.py *-example.txt /app/

RUN pip install -r requirements.txt
