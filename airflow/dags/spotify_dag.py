from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv

import os

load_dotenv(dotenv_path="opt/spotify/airflow/.env")

default_args = {
    'owner': 'bryan',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'spotify_etl_pipeline',
    default_args=default_args,
    description='Spotify Listening History ETL',
    schedule_interval="0 4,16 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    extract = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/spotify/src/extract.py'
    )

    load = BashOperator(
        task_id='load_data_to_snowflake',
        bash_command='python /opt/spotify/src/load.py'
    )
    
    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command='~/.local/bin/dbt run --project-dir /usr/app --profiles-dir /usr/app/.dbt',
        env={
            'SNOWFLAKE_ACCOUNT': os.environ.get('SNOWFLAKE_ACCOUNT'),
            'SNOWFLAKE_USER': os.environ.get('SNOWFLAKE_USER'),
            'SNOWFLAKE_ROLE': os.environ.get('SNOWFLAKE_ROLE'),
            'SNOWFLAKE_DATABASE': os.environ.get('SNOWFLAKE_DATABASE'),
            'SNOWFLAKE_WAREHOUSE': os.environ.get('SNOWFLAKE_WAREHOUSE'),
            'SNOWFLAKE_SCHEMA': os.environ.get('SNOWFLAKE_SCHEMA'),
            'SNOWFLAKE_PRIVATE_KEY_PATH': os.environ.get('SNOWFLAKE_PRIVATE_KEY_PATH'),
            },
            dag=dag,
            )


    extract >> load >> run_dbt_models
