FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt runner.sh /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/bin/env", "bash", "runner.sh"]

COPY *.py *-example.txt /app/

