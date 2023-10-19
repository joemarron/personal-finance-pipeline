# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 21:40:19 2023

@author: joema
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from transactions_to_database import add_transactions_to_temp, transform_transactions_into_db

default_args = {
    'owner': 'joe_marron',
    'start_date': datetime(2023, 10, 16),
}

dag = DAG('insert_transactions_to_CockroachDB',
          default_args=default_args,
          schedule_interval='0 7 * * *',  # Set the schedule_interval at 7am daily
          catchup=False)

add_temp = PythonOperator(
    task_id='add_temp_table_of_transactions',
    python_callable=add_transactions_to_temp,
    dag=dag
)

transform_trans = PythonOperator(
    task_id='transform_transactions_to_db',
    python_callable=transform_transactions_into_db,
    dag=dag)

add_temp>>transform_trans
