from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import func


# instanciar DAG
with DAG(dag_id='hello_dag',
         start_date=datetime(2022, 5, 23),
         schedule_interval='@hourly',
         catchup=False) as dag:

    task1 = PythonOperator(
            task_id='saludar',
            python_callable=func.saludar()
        )

task1
