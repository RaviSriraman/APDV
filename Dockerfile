FROM python:3.10-slim

WORKDIR /opt/dagster/app

COPY . /opt/dagster/app

RUN pip install -r requirements.txt

RUN ipython kernel install --name anaconda3 --user

# Run dagster gRPC server on port 4000

EXPOSE 4000

RUN mv dagster-prod.yaml dagster.yaml

RUN mv workspace-prod.yaml workspace.yaml

RUN rm .env

RUN mv prod.env .env

#VOLUME /opt/dagster/app/data

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "enterprises.definitions"]