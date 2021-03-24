from datetime import datetime
from common.utils import transform_records

# DAG default parameters
DEFAULT_ARGS = {
    "owner": "El Mehdi Belgasmi",
    "start_date": datetime(2021, 3, 21),
    "retries": 0,
}

##### DAG object config
DAG_CONFIG = {
    "dag_id": "drugs-data-pipeline",
    "description": "Drugs Data Pipeline.",
    "schedule_interval": "@once",
    "default_args": DEFAULT_ARGS,
    "catchup": False
}
# Postgres connection ID
POSTGRES_CONN_ID = "postgres_connection"

##### BEGIN Tables creation Task Group config
CREATE_TABLES_TASKS_CONFIG = {
    "group_id": "create_tables"
}

CREATE_DRUGS_TABLE_CONFIG = {
    "task_id": "create_drugs_table",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "sql": "sql/create_drugs_table.sql"
}

CREATE_PUBMED_TABLE_CONFIG = {
    "task_id": "create_pubmed_table",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "sql": "sql/create_pubmed_table.sql"
}

CREATE_CLINICAL_TRIALS_TABLE_CONFIG = {
    "task_id": "create_clinical_trials_table",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "sql": "sql/create_clinical_trials_table.sql"
}
##### END Tables creation Task Group config

##### BEGIN Database insertion Task Group config
INSERT_INTO_TABLES_TASKS_CONFIG = {
    "group_id": "insert_into_tables"
}

INSERT_CSV_INTO_DRUGS_TABLE_CONFIG = {  
    "task_id": "insert_csv_into_drugs_table",
    "file_path": "data/input/drugs.csv",
    "file_type": "csv",
    "file_delimiter": ",",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "postgres_table": "drugs"
}

INSERT_CSV_INTO_PUBMED_TABLE_CONFIG = {
    "task_id": "insert_csv_into_pubmed_table",
    "file_path": "data/input/pubmed.csv",
    "file_type": "csv",
    "file_delimiter": ",",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "postgres_table": "pubmed",
    "parse_dates": ["date"],
    "transform_id": "id"
}

INSERT_JSON_INTO_PUBMED_TABLE_CONFIG = {
    "task_id": "insert_json_into_pubmed_table",
    "file_path": "data/input/pubmed.json",
    "file_type": "json",
    "file_delimiter": ",",
    "postgres_conn_id": "postgres_connection",
    "postgres_table": "pubmed",
    "parse_dates": ["date"],
    "transform_id": "id"
}

INSERT_CSV_INTO_CLINICAL_TRIALS_TABLE_CONFIG = {
    "task_id": "insert_csv_into_clinical_trials_table",
    "file_path": "data/input/clinical_trials.csv",
    "file_type": "csv",
    "file_delimiter": ",",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "postgres_table": "clinical_trials",
    "parse_dates": ["date"]
}
##### END Database insertion Task Group config

##### BEGIN Output JSON export task config
EXPORT_DRUGS_JSON_CONFIG = {
    "task_id": "export_drugs_json",
    "postgres_conn_id": POSTGRES_CONN_ID,
    "sql": "sql/select_drugs_relations.sql",
    "transform_function": transform_records,
    "file_path": "data/output/drugs_output.json"
}
##### END Output JSON export task config