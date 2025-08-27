from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Simple function for testing
def print_hello():
    print("Hello from Airflow!")

# Default args for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Define DAG
with DAG(
    "test_dag",
    default_args=default_args,
    description="A simple test DAG",
    schedule_interval="* * * * *",  # every minute
    start_date=datetime(2025, 8, 10),
    catchup=False,
    tags=["test"],
) as dag:

    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=print_hello,
    )

    hello_task
