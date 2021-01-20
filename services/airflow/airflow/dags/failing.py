from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import random
import time

default_args = {
    'owner':'max', 
    'retries': 0,
    'email':['maxence.roux@groupe-verona.com'],
    'retry_delay':timedelta(minutes=2) , 
    'email_on_failure': True
}

dag = DAG(
    'failing_dag', 
    default_args=default_args, 
    schedule_interval=None,
    start_date=days_ago(1), 
    
)

def failing():
    time.sleep(10)
    if random.random() >= 0.5:
        print("buds")
        raise Exception("Except")
    print("genial")

t1 = PythonOperator(
    task_id='failing_dag',
    python_callable=failing, 
    dag = dag
)

t1