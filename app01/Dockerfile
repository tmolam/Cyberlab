FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask pymysql

COPY app.py .

CMD ["python", "app.py"]
