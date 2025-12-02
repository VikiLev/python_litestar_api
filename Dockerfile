FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "5000", "app.main:asgi_app"]
