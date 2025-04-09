FROM python:3.10-slim

ENV DAGSTER_HOME=/app

RUN mkdir -p $DAGSTER_HOME

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "dagster_repo/pipeline.py"]

