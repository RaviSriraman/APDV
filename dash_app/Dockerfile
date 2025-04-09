FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN rm .env
RUN mv prod.env .env

EXPOSE 8070

CMD ["python", "app.py"]

