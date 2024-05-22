from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from config.config import AIRFLOW_CONFIG
from utils.common import setup_logging, log_execution

setup_logging()

def data_collection(*args, **kwargs):
    # Implementation of data collection logic
    pass

def data_cleaning(*args, **kwargs):
    # Implementation of data cleaning logic
    pass

def data_processing(*args, **kwargs):
    # Implementation of data processing logic
    pass

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.strptime(AIRFLOW_CONFIG['start_date'], '%Y-%m-%d'),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    AIRFLOW_CONFIG['dag_id'],
    default_args=default_args,
    schedule_interval=AIRFLOW_CONFIG['schedule_interval'],
    catchup=False
) as dag:

    collect_task = PythonOperator(
        task_id='collect_data',
        python_callable=log_execution(data_collection)
    )

    clean_task = PythonOperator(
        task_id='clean_data',
        python_callable=log_execution(data_cleaning)
    )

    process_task = PythonOperator(
        task_id='process_data',
        python_callable=log_execution(data_processing)
    )

    collect_task >> clean_task >> process_task
