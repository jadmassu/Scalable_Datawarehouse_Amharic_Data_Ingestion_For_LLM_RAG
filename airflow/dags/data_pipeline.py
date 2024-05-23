from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from db.connection.db_conn import DatabaseLoader
from models.base import Database
from sqlalchemy.orm import sessionmaker
from scrapers.alain import AlainNewsScraper
from controllers.data_controller import create_data
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Initialize database connection
db_loader = DatabaseLoader()
db_loader.set_connection_url_from_dbname(Variable.get("db_database"))
db_loader.connect()
SessionLocal = sessionmaker(bind=db_loader.engine)

def scrape_news(url):
    scraper = AlainNewsScraper(url=url)
    news_data = scraper.get_full_news()
    return news_data

def save_to_database(news_data):
    session = SessionLocal()
    try:
        for article in news_data:
            db_data = create_data(session, article)
            session.add(db_data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

with DAG('news_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    scrape_task = PythonOperator(
        task_id='scrape_news_task',
        python_callable=scrape_news,
        op_kwargs={'url': Variable.get("news_scraper_url")}
    )

    save_to_db_task = PythonOperator(
        task_id='save_to_db_task',
        python_callable=save_to_database,
        op_kwargs={'news_data': "{{ task_instance.xcom_pull(task_ids='scrape_news_task') }}"}
    )

    scrape_task >> save_to_db_task

