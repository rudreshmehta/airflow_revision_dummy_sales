# Project name: Airflow_revision_dummy_sales
## Project Overview
This repository contains an Airflow project to demonstrate the use of Apache Airflow for orchestrating an ETL (Extract, Transform, Load) pipeline. The pipeline performs the following steps:

1. **Generate dummy sales data** in CSV format.
2. **Load the data** into a PostgreSQL database (staging table).
3. **Transform the data** to calculate analytics summaries (e.g., total quantity and revenue by product).
4. **Save the summary results** in an analytics table.

---

## Features
- Dynamic DAG scheduling with Airflow.
- Use of PostgresHook for database connections.
- SQL-based transformations with upsert functionality to avoid duplicate records.
- Modularized pipeline with externalized SQL queries.
- Scalable design for industry-grade workflows.

---

## Project Structure

```plaintext
├── dags/
│   ├── sample_pipeline.py         # Main Airflow DAG script
│   └── sql/
│       ├── create_staging_and_summary_tables.sql
│       └── upsert_summary_table.sql
├── Dockerfile                     # Dockerfile for Airflow setup
├── requirements.txt               # Python dependencies
├── .gitignore                     # Files to ignore in version control
└── README.md                      # Project documentation
```

---

## Technologies Used
- **Apache Airflow**: Workflow orchestration to schedule and monitor tasks.
- **PostgreSQL**: Relational database used for staging and analytics.
- **Docker**: Containerized environment for deploying Airflow and Postgres.
- **Python**: Used for scripting custom ETL logic.
- **SQL**: SQL scripts for data transformations and upserts.

---

## Getting Started

### Prerequisites
Ensure you have the following installed on your machine:
- **Docker** and **Docker Compose**: For running containers.
- **Git**: For cloning this repository and version control.

### Setup Steps
1. **Clone the Repository**:
    Clone the project to your local machine:
   ```bash
   git clone https://github.com/yourusername/airflow-sales-pipeline.git
   cd airflow-sales-pipeline
2. **Start Docker Containers**:
    Use Docker Compose to start the Airflow and PostgreSQL services:
    ```bash
    docker-compose up -d
    ```
    - An Airflow webserver on http://localhost:8080.
    - A PostgreSQL database accessible on localhost:5432
3. **Access the Airflow UI**:
   Open your browser and navigate to _http://localhost:8080_.
   Log in with the default credentials:
    - Username: admin
    - Password: admin
5. **Set Up Airflow Connections**:
   Create a new connection in the Airflow UI for PostgreSQL:
    1. Go to **Admin > Connections**.
    2. Click **+ Add a new record**.
    3. Configure as follows:
       - **Conn ID**: `postgres_default`
       - **Conn Type**: `Postgres`
       - **Host**: `postgres`
       - **Schema**: `pgwh`
       - **Login**: `postgres`
       - **Password**: `postgres`
       - **Port**: `5432`
5. **Run the Pipeline**:
    1. In the Airflow UI, locate the `sales_pipeline` DAG.
    2. Turn it on using the toggle switch.
    3. Trigger the DAG manually by clicking the play button (▶️).
6. **Verify Results**:
    After the pipeline runs, log into the PostgreSQL database to check the data:
      ```bash
      docker exec -it postgres-container psql -U postgres -d pgwh

**I would be throwing more examples in the future. It is open to fork or contribute in order to make it a rich source of learning the data engineering.** `Thank you`


