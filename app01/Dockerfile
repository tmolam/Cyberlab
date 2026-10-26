FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask pymysql \
    && useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser app.py .

USER appuser

CMD ["python", "app.py"]
