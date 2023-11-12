FROM python:3.11.5

WORKDIR simple-movie-database

ENV ENVIRONMENT local

RUN pip install pipenv

RUN apt-get update && apt-get -y install supervisor

RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /usr/bin/cloud_sql_proxy
RUN chmod +x /usr/bin/cloud_sql_proxy

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile

ADD src src
ADD service_secrets service_secrets

COPY config.py .
COPY run.py .
COPY supervisord.conf .

EXPOSE 8080

CMD ["supervisord", "-c", "supervisord.conf"]
