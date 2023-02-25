from pathlib import Path
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from datetime import timedelta

@task(log_prints=True, retries=3)
def fetch_files(url: str, file: str, color: str) -> Path:
    """ Task that retrive all the files linked in the input url """
    if color!="":
        path = Path(f"data/{color}")
    else:
        path = Path("data/fhv")

    path.mkdir(parents=True, exist_ok=True)
    file_path = path / file
    os.system(f"wget {url} -O {file_path}")
    return file_path

@task(log_prints=True)
def write_on_gcs(path: Path, bucket_name: str) -> None:
    """ Task thath use Prefect Gcp Bucket to store the data retrived from the previous task to gcs """
    gcs_block = GcsBucket.load(bucket_name)
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def web_to_gcs(color, month, year, bucket):
    """ Main function """
    if color=="":
        file = f"fhv_tripdata_{year}-{month:02}.csv.gz"
        url = f"fhv/{file}"
    else:
        file = f"{color}_tripdata_{year}-{month:02}.csv.gz"
        url = f"{color}/{file}"
    
    dataset_file = file
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{url}"

    path = fetch_files(dataset_url, dataset_file, color)
    write_on_gcs(path, bucket)

@flow()
def parent_flow(color: str="", months: list[int]=[1], year: int=2023, bucket: str=""):
    for month in months:
        web_to_gcs(color, month, year, bucket)

if __name__ == '__main__':
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    year=2019
    color="yellow"
    bucket="week-4-lessons"
    parent_flow(color, months, year, bucket)
