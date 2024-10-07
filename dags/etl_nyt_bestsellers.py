from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from dotenv import load_dotenv
import os
import json
import pandas as pd
import sqlalchemy as db


def transform_func(ti):
    value = ti.xcom_pull(task_ids='extract')
    data = json.loads(value)
    data = pd.DataFrame(data['results']['books'])
    
    cols_to_keep =  ['rank', 'rank_last_week', 'weeks_on_list', 'publisher', 'description', 'title', 'author']
    data = data[cols_to_keep]
    
    return data

load_dotenv()
password = os.getenv('PASSWORD')
engine = db.create_engine(f'postgresql://postgres.qhuhevlwiyybwidxuihs:{password}@aws-0-us-west-1.pooler.supabase.com:6543/postgres'.format(password))


def load_func(ti):
    value = ti.xcom_pull(task_ids='transform')
    value.to_sql('hardcover_fiction_bestseller', engine, if_exists='replace', index=False)
    print('Loaded into database!')
    

default_args = {
   'owner': 'siqi',
   'start_date': datetime(2024, 9, 1),
   'schedule_interval': '@once',
}


with DAG(
    dag_id = 'etl_new_york_times_hardcover_fiction_bestseller',
    description = 'New York Times bestseller list for hardcover-fiction',
    default_args = default_args,
    catchup = False
) as dag:
    
    extract = BashOperator(
        task_id = 'extract',
        bash_command = '''
        python3 /Users/liusiqi/airflow/extract_python_scripts/extract_nyt_bestsellers.py
        '''
    )
    
    transform = PythonOperator(
        task_id = 'transform',
        python_callable = transform_func
    )
    
    load = PythonOperator(
        task_id = 'load',
        python_callable = load_func
    )
 
extract >> transform >> load
