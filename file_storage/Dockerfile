FROM python:3.12-slim

WORKDIR /app
RUN pip install gunicorn==20.1.0 
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
COPY . .

COPY gunicorn.conf.py ./gunicorn.conf.py
