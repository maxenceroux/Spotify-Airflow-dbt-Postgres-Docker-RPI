from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import random

default_args = {
    'owner':'max',
    'retries':1,
    'retry_delay': timedelta(seconds=5)
}

dag = DAG(
    'my_test_dag',
    default_args=default_args,
    schedule_interval=None, 
    start_date=days_ago(1)
)

def my_func(**context):
    print("hi")
    context['ti'].xcom_push(key="my_key", value=random.random())

def my_func_xcom(**context):
    print("hello")
    returned_value = context['ti'].xcom_pull(key="my_key")
    print(returned_value)


t1 = PythonOperator(
    task_id='t1',
    python_callable=my_func, 
    provide_context=True, 
    dag = dag
)

t2 = PythonOperator(
    task_id='t2',
    python_callable=my_func_xcom,
    provide_context=True, 
    dag = dag
)

t1 >> t2