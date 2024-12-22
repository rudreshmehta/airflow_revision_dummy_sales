from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2

def extract_data():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

def transform_data(data):
    return [{"id": item["id"], "name": item["name"].upper()} for item in data]

def load_data(data):
    connection = psycopg2.connect(
        dbname="pgwh",
        user="postgres",
        password="postgres",
        host="postgres",
        port=5432
    )
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT);")
    for item in data:
        cursor.execute(
            "INSERT INTO users (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;",
            (item["id"], item["name"])
        )
    connection.commit()
    cursor.close()
    connection.close()

with DAG(
    dag_id="example_etl_pipeline",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
        op_args=[extract_task.output],
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_data,
        op_args=[transform_task.output],
    )

    extract_task >> transform_task >> load_task



# Testing block to check python functions directly
# if __name__ == "__main__":
#     data = extract_data()
#     print("Extracted Data:", data)

#     transformed_data = transform_data(data)
#     print("Transformed Data:", transformed_data)

#     load_data(transformed_data)
#     print("Data loaded into PostgreSQL!")