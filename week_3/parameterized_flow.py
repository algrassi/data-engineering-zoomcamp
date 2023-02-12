from pathlib import Path
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from datetime import timedelta

@task(retries=3, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str, dataset_file: str) -> Path:
    p = Path(f"data/fhv/")
    p.mkdir(parents=True, exist_ok=True)
    file_name = f"{dataset_file}.csv.gz"
    file_path = p / file_name
    os.system(f"wget {dataset_url} -O data/fhv/{file_name}")
    return file_path

@task()
def write_gcs(path: Path) -> None:
    """Uploading local parquet file to GCS"""
    gcs_block = GcsBucket.load("week-3")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def etl_web_to_gcs(year: int, month: int) -> None:
    """The main ETL function"""
    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"

    path = fetch(dataset_url, dataset_file)
    write_gcs(path)

@flow()
def etl_parent_flow(months: list[int] = [1, 2], year: int = 2021):
    for month in months:
        etl_web_to_gcs(year, month)

if __name__ == '__main__':
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    year=2019
    etl_parent_flow(months, year)