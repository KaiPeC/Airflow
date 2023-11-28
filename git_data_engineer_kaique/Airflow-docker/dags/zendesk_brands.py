from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash import BashOperator


seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                    datetime.min.time())

default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': seven_days_ago,
        'email': ['airflow@airflow.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
}

dag = DAG('brands_zendesk', default_args=default_args,schedule_interval="05 10-21/5 * * 1-6",)

pokelist = BashOperator(
    task_id = "pokelist",
    bash_command='python3 /opt/airflow/scripts/zendesk/brands/brands.py',
    dag=dag
        
)


