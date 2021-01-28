"""
### Example HTTP operator and sensor
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators import SimpleHttpOperator

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import os
import json
import requests

default_args = {
    'owner': 'rax',
    'depends_on_past': False,
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=1),
}

dag = DAG('get_song_info', default_args=default_args,schedule_interval=None,
    start_date=days_ago(1))


dag.doc_md = __doc__


def get_untracked_songs(**context):
    src = PostgresHook(postgres_conn_id='dbt_postgres_instance_raw_data')
    src_conn = src.get_conn()
    cursor = src_conn.cursor()
    cursor.execute("SELECT DISTINCT spotify_id FROM song where spotify_id IS NOT NULL;")
    songs = cursor.fetchall()
    songs_reformated = ""
    for s in songs:
        songs_reformated = songs_reformated+f";{s[0]}"
    songs_reformated = songs_reformated[1:]
    context['ti'].xcom_push(key="my_songs", value=songs)

    return songs


def get_songs_info(**context):
    song_ids = context['ti'].xcom_pull(key="my_songs")
    token = json.loads(context['task_instance'].xcom_pull(task_ids='get_token'))['access_token']
    print(token)
    url = f"https://api.spotify.com/v1/audio-features/?id={song_ids}"
    headers = {
    'Accept': 'application/json',    
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()


    
t1a = PythonOperator(
    task_id='get_songs',
    python_callable=get_untracked_songs,
    provide_context=True,
    dag = dag
)
t1b = SimpleHttpOperator(
    task_id='get_token', 
    method='POST', 
    http_conn_id='spotify',
    endpoint='token',
    headers={"accept": "application/json", "Content-Type":"application/x-www-form-urlencoded"},
    data={'username':'maxence','password':'maxence'},
    xcom_push=True
)


t2 = PythonOperator(
    task_id='get_songs_info',
    python_callable=get_songs_info,
    provide_context=True,
    dag = dag
)

t1a >> t2
t1b >> t2
