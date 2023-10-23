FROM python:3.9

RUN apt-get update \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
    
RUN pip install pandas sqlalchemy psycopg2 fastparquet

WORKDIR /app
COPY ingest-data.py ingest-data.py

ENTRYPOINT [ "python", "ingest-data.py" ]