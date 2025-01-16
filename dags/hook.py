import pandas as pd
import logging

from airflow.models import DAG
from airflow.utils import dates
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    'start_date': dates.days_ago(1)
}

def getPandas():
    conn = PostgresHook('redshift_produccion')
    df = conn.get_pandas_df("SELECT * FROM TABLE")
    logging.info("Datos obtenidos en la query")

with DAG(dag_id='dag_hooks',
         default_args=default_args,
         schedule_interval='@daily') as dag:

    start = EmptyOperator(task_id='start')

    getPandasOperator = PythonOperator(task_id='getPandasOperator',
                                       python_callable=getPandas)
    end = EmptyOperator(task_id='end')

start >> getPandasOperator >> end