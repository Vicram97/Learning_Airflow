from datetime import datetime

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'victor_ramos',
    'start_date': datetime(2025, 1, 15, 11, 0, 0)
}


def hello_world_loop():
    for palabra in ['hello', 'world']:
        print(palabra)


with DAG('hello_victor',
         default_args=default_args,
         schedule_interval='@daily') as dag:
    start = DummyOperator(task_id='start')

    prueba_python = PythonOperator(task_id='prueba_python',
                                   python_callable=hello_world_loop)

    prueba_bash = BashOperator(task_id='prueba_bash',
                               bash_command='echo prueba_bash')

start >> prueba_python >> prueba_bash