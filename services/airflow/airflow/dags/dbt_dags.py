from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# [START default_args]
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}
# [END default_args]

# [START instantiate_dag]
most_listened = DAG(
    'most_listened_dbt',
    catchup=False,
    default_args=default_args,
    description='Get most listened',
    schedule_interval="0 4 * * *",
)

bsh_cmd = 'cd /dbt && dbt run'


tmp_operator = BashOperator(task_id='most_listened',
                            bash_command=bsh_cmd,
                            dag=most_listened,
                            depends_on_past=True
                            )

tmp_operator
