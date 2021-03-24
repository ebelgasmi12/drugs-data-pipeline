from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.operators.postgres import PostgresOperator
from common.plugins.postgres.operators import FileToPostgresOperator
from common.plugins.postgres.operators import PostgresToJSONOperator
from drugs_data_pipeline.config import (
    DAG_CONFIG, CREATE_TABLES_TASKS_CONFIG, CREATE_DRUGS_TABLE_CONFIG,
    CREATE_PUBMED_TABLE_CONFIG, CREATE_CLINICAL_TRIALS_TABLE_CONFIG,
    INSERT_INTO_TABLES_TASKS_CONFIG, INSERT_CSV_INTO_DRUGS_TABLE_CONFIG,
    INSERT_CSV_INTO_PUBMED_TABLE_CONFIG, INSERT_JSON_INTO_PUBMED_TABLE_CONFIG,
    INSERT_CSV_INTO_CLINICAL_TRIALS_TABLE_CONFIG,
    EXPORT_DRUGS_JSON_CONFIG
)


##### DAG object initialization
with DAG(**DAG_CONFIG) as dag:
    
    ##### BEGIN Tables creation Task Group
    with TaskGroup(**CREATE_TABLES_TASKS_CONFIG) as create_tables_tasks:
        create_drugs_table = \
            PostgresOperator(**CREATE_DRUGS_TABLE_CONFIG)
        create_pubmed_table = \
            PostgresOperator(**CREATE_PUBMED_TABLE_CONFIG)
        create_clinical_trials_table = \
            PostgresOperator(**CREATE_CLINICAL_TRIALS_TABLE_CONFIG)
    ##### END Tables creation Task Group
    
    ##### BEGIN Database insertion Task Group
    with TaskGroup(**INSERT_INTO_TABLES_TASKS_CONFIG) as insert_into_tables:
        insert_csv_into_drugs_table = \
            FileToPostgresOperator(**INSERT_CSV_INTO_DRUGS_TABLE_CONFIG)
        insert_csv_into_pubmed_table = \
            FileToPostgresOperator(**INSERT_CSV_INTO_PUBMED_TABLE_CONFIG)
        insert_json_into_pubmed_table = \
            FileToPostgresOperator(**INSERT_JSON_INTO_PUBMED_TABLE_CONFIG)
        insert_csv_into_clinical_trials_table = \
        FileToPostgresOperator(**INSERT_CSV_INTO_CLINICAL_TRIALS_TABLE_CONFIG)
    ##### END Database insertion Task Group
    
    ##### BEGIN Output JSON export task
    export_drugs_json = \
        PostgresToJSONOperator(**EXPORT_DRUGS_JSON_CONFIG)
    ##### END Output JSON export task

    ##### BEGIN DAG creation
    create_drugs_table >> insert_csv_into_drugs_table
    create_pubmed_table >> [insert_csv_into_pubmed_table, 
                            insert_json_into_pubmed_table]
    create_clinical_trials_table >> insert_csv_into_clinical_trials_table
    insert_into_tables >> export_drugs_json
    ##### END DAG creation