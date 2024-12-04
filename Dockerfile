FROM python:3.10-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

CMD ["python", "rest_server.py"]
