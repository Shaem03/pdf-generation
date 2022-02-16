FROM python:3.8.0-slim

MAINTAINER shaheem@cloudloom.io

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y

RUN apt-get install gunicorn3 -y

RUN apt-get install wkhtmltopdf -y

ADD . /app/

WORKDIR /app/

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5", "--timeout=300"]
#CMD ["python3", "app.py"]