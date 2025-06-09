from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

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
    schedule_interval='30 23 * * *',
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

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='dbt run --project-dir /opt/spotify/dbt'
    )

    extract >> load >> run_dbt
