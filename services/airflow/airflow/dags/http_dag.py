"""
### Example HTTP operator and sensor
"""
from airflow import DAG
from airflow.operators import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import os
import json
import requests

default_args = {
    'owner': 'raxpotify',
    'depends_on_past': False,
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=1),
}

dag = DAG('get_spotify_songs',catchup=False, default_args=default_args,schedule_interval="*/20 * * * *",
    start_date=days_ago(1))
# dag = DAG('get_spotify_songs', default_args=default_args,schedule_interval=None,
#     start_date=days_ago(1))


dag.doc_md = __doc__

# t1, t2 and t3 are examples of tasks created by instatiating operators
t1 = SimpleHttpOperator(
    task_id='get_token', 
    method='POST', 
    http_conn_id='spotify',
    endpoint='token',
    headers={"accept": "application/json", "Content-Type":"application/x-www-form-urlencoded"},
    # data={'username':os.environ['MY_USERNAME'],'password':os.environ['MY_PASSWORD']},
    data={'username':'maxence','password':'maxence'},
    xcom_push=True
)


def get_songs(**context):
    print(json.loads(context['task_instance'].xcom_pull(task_ids='get_token')))
    token = json.loads(context['task_instance'].xcom_pull(task_ids='get_token'))['access_token']
    url = "http://web:8000/songs"
    headers={"accept": "application/json","Authorization": f"Bearer {token}"}
    response = requests.request("GET", url, headers=headers)
    return response.status_code

t2 = PythonOperator(
    task_id='get_songs',
    python_callable=get_songs,
    provide_context=True,
    dag = dag
)


t1 >> t2 