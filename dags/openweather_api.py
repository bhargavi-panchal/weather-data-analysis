from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
import boto3

# --------------------------
# Default DAG arguments
# --------------------------
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 12),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# --------------------------
# DAG definition
# --------------------------
dag = DAG(
    dag_id='openweather_api_dag',
    default_args=default_args,
    schedule="@once",
    catchup=False,
)

# --------------------------
# OpenWeather API setup
# --------------------------
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_PARAMS = {
    "q": "Toronto,Canada",
    "appid": Variable.get("api_key"),
}

S3_BUCKET = "weather-data-project-gds"

# --------------------------
# Extract + Load to S3 (boto3)
# --------------------------
def extract_and_upload_to_s3(ds, **kwargs):
    print("Starting OpenWeather API extraction...")

    response = requests.get(API_ENDPOINT, params=API_PARAMS)
    response.raise_for_status()

    data = response.json()

    if "list" not in data or not data["list"]:
        raise ValueError("No forecast data returned from API")

    df = pd.json_normalize(data["list"])
    print(f"Extracted {len(df)} rows")

    csv_data = df.to_csv(index=False)

    s3_key = f"date={ds}/weather_api_data.csv"
    print(f"Uploading to s3://{S3_BUCKET}/{s3_key}")

    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=csv_data.encode("utf-8"),
        ContentType="text/csv"
    )

    print("Upload successful")

# --------------------------
# Tasks
# --------------------------
extract_and_upload = PythonOperator(
    task_id="extract_and_upload_weather_data",
    python_callable=extract_and_upload_to_s3,
    dag=dag,
)

trigger_transform_redshift_dag = TriggerDagRunOperator(
    task_id="trigger_transform_redshift_dag",
    trigger_dag_id="transform_redshift_dag",
    dag=dag,
)

# --------------------------
# Task dependencies
# --------------------------
extract_and_upload >> trigger_transform_redshift_dag
