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
    data = pd.DataFrame(data['response']['docs'])
    
    cols_to_keep = ['abstract', 'web_url', 'headline', 'pub_date', 'document_type', 
                    'news_desk', 'section_name', 'subsection_name', 'byline', 
                    'type_of_material', 'word_count']
    data = data[cols_to_keep]
    
    data['headline'] = data['headline'].apply(lambda x: x['main'])
    data['byline'] = data['byline'].apply(lambda x: x['original'][2:])
    data['pub_date'] = pd.to_datetime(data['pub_date'])
    
    return data

load_dotenv()
password = os.getenv('PASSWORD')
engine = db.create_engine(f'postgresql://postgres.qhuhevlwiyybwidxuihs:{password}@aws-0-us-west-1.pooler.supabase.com:6543/postgres'.format(password))


def load_func(ti):
    value = ti.xcom_pull(task_ids='transform')
    value.to_sql('articles_of_current_month', engine, if_exists='replace', index=False)
    print('Loaded into database!')
 

default_args = {
   'owner': 'siqi',
   'start_date': datetime(2024, 9, 1),
   'schedule_interval': '@once',
}

with DAG(
    dag_id = 'etl_new_york_times_articles_of_the_current_month',
    description = 'New York Times articles of the current month',
    default_args = default_args,
    catchup = False
) as dag:
    
    extract = BashOperator(
        task_id = 'extract',
        bash_command = '''
        python3 /Users/liusiqi/airflow/extract_python_scripts/extract_nyt_articles.py
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
