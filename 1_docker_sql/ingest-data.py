#!/usr/bin/env python
# coding: utf-8
# this file is created from cli with 'jupyter nbconvert' commamd

import pandas as pd
import os
import argparse
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url
    parquet_name = 'output.parquet'

    os.system(f'wget {url} -O {parquet_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df = pd.read_parquet(parquet_name, engine='fastparquet')

    df.head(n=0).to_sql(name=table, con=engine, if_exists='replace')
    df.to_sql(name=table, con=engine, if_exists='append')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest parquet data to Postgres")

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='databse name for postgres')
    parser.add_argument('--table', help='name of the table where we will write the result to')
    parser.add_argument('--url', help='url of the parquet file')

    args = parser.parse_args()
    print(args)
    main(args)