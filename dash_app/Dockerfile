FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install zlib1g-dev -y
RUN apt-get install gcc python3-dev -y

RUN pip install --no-cache-dir -r requirements.txt

RUN rm .env
RUN mv prod.env .env
RUN rm src/.env
RUN mv src/prod.env src/.env

EXPOSE 8070

CMD ["python", "src/app.py"]

