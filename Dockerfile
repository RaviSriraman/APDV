FROM python:3.12

LABEL authors="ravisreeraman"

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin:$PATH"
ENV PATH="/opt/app/bin:$PATH"
ENV DAGSTER_HOME=/opt/app

RUN mkdir /opt/app
RUN mkdir /opt/app/bin

COPY . /opt/app
COPY bin/run.sh /opt/app/bin/

WORKDIR /opt/app

RUN rm run.sh

RUN pip3 install --upgrade setuptools pip wheel

RUN pip3 install --extra-index-url https://pypi.fury.io/arrow-nightlies/ \
        --prefer-binary --pre pyarrow

RUN pip3 install dagster dagster-webserver pandas seaborn pymongo

RUN uv sync

EXPOSE 3000

VOLUME data abc/

RUN chmod +x /opt/app/bin/run.sh

#CMD ["run.sh"]