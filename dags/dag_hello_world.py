from datetime import datetime
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Victor Ramos Fuentes',
    'start_date' : datetime(2025, 1, 14, 11, 0, 0)
}

def hello_world_loop():
    for palabra in ['hello', 'world']:
        print(palabra)

with DAG (
    dag_id = 'dag_hello_world',
    default_args = default_args,
    schedule_interval = '@once',
    ) as dag:

    start = EmptyOperator(task_id='hello_world')
    ptyOp = PythonOperator(task_id='python_hello_world', python_callable=hello_world_loop)
    bashOp = BashOperator(task_id='bash_hello_world', bash_command='echo "Hello Bash World!"')

start >> ptyOp >> bashOp