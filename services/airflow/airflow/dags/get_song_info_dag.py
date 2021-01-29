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
import base64

default_args = {
    'owner': 'rax',
    'depends_on_past': False,
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=1),
}

dag = DAG('get_song_info',catchup=False,default_args=default_args,schedule_interval='0 */6 * * *',
    start_date=days_ago(1))

dag.doc_md = __doc__


def get_untracked_songs(**context):
    src = PostgresHook(postgres_conn_id='dbt_postgres_instance_raw_data')
    src_conn = src.get_conn()
    cursor = src_conn.cursor()
    cursor.execute("SELECT max(added_at) from song;")    
    cursor.execute("SELECT max(added_at) from song;")
    if cursor.fetchone()[0] != None: ts = cursor.fetchone()[0]
    else: ts = datetime.now() - timedelta(days=720)
    cursor.execute(f"SELECT DISTINCT spotify_id FROM listen where spotify_id IS NOT NULL and ts >= '{ts}';")
    songs = cursor.fetchall()
    songs_reformated = ""
    for s in songs:
        songs_reformated = songs_reformated+f",{s[0]}"
    songs_reformated = songs_reformated[1:]
    context['ti'].xcom_push(key="my_songs", value=songs_reformated)

    return songs

def get_spotify_token(**context):
    url = "https://accounts.spotify.com/api/token"
    credentials = os.environ['SPOTIPY_CLIENT_ID']+":"+os.environ['SPOTIPY_CLIENT_SECRET']
    encoded_spotify_token = base64.b64encode(bytes(credentials, 'utf-8'))
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {encoded_spotify_token.decode("utf-8")}'
    }
    payload = {'grant_type':'client_credentials'}
    response = requests.request("POST", url, headers=headers, data=payload)
    context['ti'].xcom_push(key="spotify_token", value=response.json()['access_token'])
    return response.json()['access_token']

def get_songs_info(**context):
    song_ids = context['ti'].xcom_pull(key="my_songs")
    token =  context['ti'].xcom_pull(key="spotify_token")
    url = f"https://api.spotify.com/v1/audio-features/?ids={song_ids}"
    headers = {
    'Accept': 'application/json',    
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers)
    res = response.json()['audio_features'] 
    keys_to_remove = ['analysis_url', 'type',  'uri', 'track_href', 'time_signature']
    features_list = []
    if res[0]!=None:
        for song in res:
            for key in keys_to_remove:
                song.pop(key)
            features_list.append(song)
        url = f"https://api.spotify.com/v1/tracks?ids={song_ids}"
        response = requests.request("GET", url, headers=headers)
        res = response.json()['tracks']
        songs_list = []
        for song in res: 
            songs_list.append({
                "album_name": song['album']['name'],
                "artist": song['album']['artists'][0]['name'],
                "name": song['name'],
                "id": song['id'],
                "popularity": song['popularity']
            })
        merged_li = []
        for i in range(len(features_list)):
            merged_li.append(dict(songs_list[i],**features_list[i]))
        for item in merged_li:
            item['spotify_id'] = item.pop('id')
            item['duration'] = item.pop('duration_ms')
    else: merged_li = []
    merged_to_send = {"songs":merged_li}
    context['ti'].xcom_push(key="songs_info", value=merged_to_send)
    return merged_to_send

def upload_to_pgsql(**context):
    songs = context['ti'].xcom_pull(key="songs_info")
    url = "http://web:8000/song"
    # headers={"accept": "application/json"}
    response = requests.request("POST", url, data = json.dumps(songs))
    print(songs)
    return response.content

t1a = PythonOperator(
    task_id='get_songs',
    python_callable=get_untracked_songs,
    provide_context=True,
    dag = dag
)
t1b = PythonOperator(
    task_id='get_token',
    python_callable=get_spotify_token,
    provide_context=True,
    dag = dag
)


t2 = PythonOperator(
    task_id='get_songs_info',
    python_callable=get_songs_info,
    provide_context=True,
    dag = dag
)

t3 = PythonOperator(
    task_id='upload_to_db',
    python_callable=upload_to_pgsql,
    provide_context=True,
    dag=dag
)
t1a >> t2 >> t3
t1b >> t2 >> t3
