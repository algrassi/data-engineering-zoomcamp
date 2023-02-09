from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> pd.DataFrame:
    """Download trip data from GCS"""
    gcs_path=f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./")
    p = Path(f"./{gcs_path}")
    df = pd.read_parquet(p)
    return df

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    df.to_gbq(
        destination_table="dezoomcamp.yellow_rides",
        project_id="helical-ascent-375912",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow(log_prints=True)
def etl_gcs_to_bq(color:str, year:int, month:int):
    """Main ETL flow to load data into Big Query"""
    df = extract_from_gcs(color, year, month)
    print(f"rows: {len(df)}")
    write_bq(df)

@flow(log_prints=True)
def etl_parent_flow(months: list[int]=[1,2], year: int=2021, color: str="yellow"):
    for month in months:
        etl_gcs_to_bq(color, year, month)   

if __name__ == "__main__":
    etl_parent_flow()