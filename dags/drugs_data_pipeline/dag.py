from airflow.models import DAG
from datetime import datetime
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.operators.postgres import PostgresOperator
from common.plugins.postgres.operators import FileToPostgresOperator
from common.plugins.postgres.operators import PostgresToJSONOperator
from common.utils import transform_records

# DAG default parameters
default_args = {
    "owner": "El Mehdi Belgasmi",
    "start_date": datetime(2021, 3, 21),
    "retries": 0,
}
##### DAG object initialization
with DAG(dag_id="drugs-data-pipeline",
         description="Drugs Data Pipeline.",
         schedule_interval="@once", 
         default_args=default_args,
         catchup=False) as dag:
    
    ##### BEGIN Tables creation Task Group
    with TaskGroup(group_id="create_tables") as create_tables_tasks:
        create_drugs_table = PostgresOperator(
            task_id="create_drugs_tsable",
            postgres_conn_id="postgres_connection",
            sql="sql/create_drugs_table.sql",
        )
        create_pubmed_table = PostgresOperator(
            task_id="create_pubmed_table",
            postgres_conn_id="postgres_connection",
            sql="sql/create_pubmed_table.sql",
        )
        create_clinical_trials_table = PostgresOperator(
            task_id="create_clinical_trials_table",
            postgres_conn_id="postgres_connection",
            sql="sql/create_clinical_trials_table.sql",
        )
    ##### END Tables creation Task Group
    
    ##### BEGIN Database insertion tasks
    with TaskGroup(group_id="insert_into_tables") as insert_into_tables:
        insert_csv_into_drugs_table = FileToPostgresOperator(
            task_id="insert_csv_into_drugs_table",
            file_path="data/input/drugs.csv",
            file_type="csv",
            file_delimiter=",",
            postgres_conn_id="postgres_connection",
            postgres_table="drugs"
        )
        insert_csv_into_pubmed_table = FileToPostgresOperator(
            task_id="insert_csv_into_pubmed_table",
            file_path="data/input/pubmed.csv",
            file_type="csv",
            file_delimiter=",",
            postgres_conn_id="postgres_connection",
            postgres_table="pubmed",
            parse_dates=["date"],
            transform_id="id"
        )
        insert_json_into_pubmed_table = FileToPostgresOperator(
            task_id="insert_json_into_pubmed_table",
            file_path="data/input/pubmed.json",
            file_type="json",
            postgres_conn_id="postgres_connection",
            postgres_table="pubmed",
            parse_dates=["date"],
            transform_id="id"
        )
        insert_csv_into_clinical_trials_table = FileToPostgresOperator(
            task_id="insert_csv_into_clinical_trials_table",
            file_path="data/input/clinical_trials.csv",
            file_type="csv",
            file_delimiter=",",
            postgres_conn_id="postgres_connection",
            postgres_table="clinical_trials",
            parse_dates=["date"]
        )
    ##### END Database insertion tasks
    
    ##### BEGIN Output JSON export task
    export_drugs_json = PostgresToJSONOperator(
        task_id="export_drugs_json",
        postgres_conn_id="postgres_connection",
        sql="sql/select_drugs_relations.sql",
        transform_function=transform_records,
        file_path="data/output/drugs_output.json",
    )
    ##### END Output JSON export task

    ##### BEGIN DAG creation
    create_drugs_table >> insert_csv_into_drugs_table
    create_pubmed_table >> [insert_csv_into_pubmed_table, 
                            insert_json_into_pubmed_table]
    create_clinical_trials_table >> insert_csv_into_clinical_trials_table
    insert_into_tables >> export_drugs_json
    ##### END DAG creation