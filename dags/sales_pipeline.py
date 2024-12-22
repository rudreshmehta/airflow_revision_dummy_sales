from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import csv
import os

# Define file path
FILE_PATH  = "/opt/airflow/dags/sales_data.csv"
# sql_dir    = "/opt/airflow/dags/sql"

def validate_csv():
    import pandas as pd
    df = pd.read_csv(FILE_PATH)
    if df.isnull().values.any():
        raise ValueError("CSV contains null values!")

# notify failure
def notify_failure(context):
    import logging
    logging.error(f"NOTIFICATION-------------- Task failed: {context['task_instance'].task_id}")

# Dummy data for simulation
def generate_csv():
    rows = [
        ["1", "Alice", "Laptop", "2", "1000", "2023-12-15"],
        ["2", "Bob", "Mouse", "5", "25", "2023-12-15"],
        ["3", "Alice", "Keyboard", "3", "50", "2023-12-16"]
    ]
    with open(FILE_PATH, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["order_id", "customer_name", "product", "quantity", "price", "order_date"])
        writer.writerows(rows)

# Python task: Load CSV data into Postgres
def load_csv_to_postgres():
    # import psycopg2
    # conn = psycopg2.connect(
    #     dbname="pgwh", user="postgres", password="postgres", host="postgres", port="5432"
    # )
    # cursor = conn.cursor()

    # this will fetch the postgres connection done on airflow gui or cli
    # therefore only single source of connection object instead of manually connecting via psycopg2
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = postgres_hook.get_conn() 
    cursor = conn.cursor()

    try:
        with open(FILE_PATH, "r") as file:
            # next(file)  # Skip header row
            cursor.copy_expert(
            """
            COPY staging_sales (order_id, customer_name, product, quantity, price, order_date)
            FROM STDIN WITH CSV HEADER
            """, 
            file
        )
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Failed to load CSV into Postgres: {str(e)}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# DAG definition
with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2024, 12, 15),
    schedule_interval="@daily",
    catchup=False
) as dag:

    generate_csv_task = PythonOperator(
        task_id="generate_csv",
        python_callable=generate_csv,
        on_failure_callback=notify_failure
    )

    create_staging_table_task = PostgresOperator(
        task_id = "create_staging_table",
        postgres_conn_id = "postgres_default",
        sql = "sql/create_staging_and_summary_tables.sql", # os.path.join(sql_dir, "create_staging_and_summary_tables.sql"),
        on_failure_callback=notify_failure
    )
    
    load_csv_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres,
        on_failure_callback=notify_failure
    )

    create_summary_task = PostgresOperator(
        task_id="create_summary_table",
        postgres_conn_id="postgres_default",
        sql="upsert_summary_table.sql", # os.path.join(sql_dir, "upsert_summary_table.sql")
        on_failure_callback=notify_failure
    )

    generate_csv_task >> create_staging_table_task >> load_csv_task >> create_summary_task
