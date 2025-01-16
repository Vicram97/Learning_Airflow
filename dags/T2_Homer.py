from datetime import datetime
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'HomerSimpson',
    'start_date' : datetime(2025, 1, 14, 11, 0, 0)
}

def redaccionHomer():
    print("El uso de Airflow en la universidad de Springfield.\n")
    print("El otro día mi hija me dijo que Airflow no se utilizaba en la universidad de Springfield, y yo le dije: qué no Lisa? qué no?.\n")
    print(("Púdrete Flanders\n" * 150).strip())


with DAG (
    dag_id = 'dag_Homer',
    default_args = default_args,
    schedule_interval = '@daily',
    ) as dag:

    start = EmptyOperator(task_id='homer')
    ptyOp = PythonOperator(task_id='python_homer', python_callable=redaccionHomer)
    bashOp = BashOperator(task_id='bash_homer', bash_command='echo "Homer2"')

start >> ptyOp >> bashOp