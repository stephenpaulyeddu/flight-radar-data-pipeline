from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timezone
import sys
import os
from flight_radar.update_database import check_collection, add_new_flights, update_non_landed_flights, update_non_takeoff_flights

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "add_new_flights_dag",
    default_args=default_args,
    description="Add new flights every 5 minutes",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2025, 8, 27, tzinfo=timezone.utc),
    catchup=False,
) as dag:

    create_collection_task = PythonOperator(
        task_id="create_collection",
        python_callable=check_collection,
    )

    add_new_flights_task = PythonOperator(
        task_id="add_new_flights",
        python_callable=lambda **context: add_new_flights(
            context["data_interval_end"]
        ),
    )

    update_non_landed_flights_task = PythonOperator(
        task_id="update_non_landed_flights",
        python_callable=lambda **context: update_non_landed_flights(
            context["data_interval_end"]
        ),
    )

    update_non_takeoff_flights_task = PythonOperator(
        task_id="update_non_takeoff_flights",
        python_callable=lambda **context: update_non_takeoff_flights(
            context["data_interval_end"]
        ),
    )

    create_collection_task >> [ add_new_flights_task, update_non_landed_flights_task, update_non_takeoff_flights_task ]
