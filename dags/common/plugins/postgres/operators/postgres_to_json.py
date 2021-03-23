from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
from common.utils import get_absolute_path

class PostgresToJSONOperator(BaseOperator):
    """
    Airflow Operator that gets data from a PostgreSQL 
    database, transforms it and inserts it into a file.
    :param sql: SQL query to fetch data.
    :param postgres_conn_id: Airflow Connection ID.
    :param transform_function: Python transformation function (Callable).
        Takes 1 argument (records) and returns transformed records.
    :param file_path: Output file path.    
    """

    template_fields = ('sql',)
    template_fields_renderers = {'sql': 'sql'}
    template_ext = ('.sql',)
    
    def __init__(self, sql, transform_function, file_path,
                 postgres_conn_id="postgres_default",
                 *args, **kwargs):
        # Call super class constructor
        super(PostgresToJSONOperator, self).__init__(*args, **kwargs)
        # Set new attributes
        self.sql = sql
        self.postgres_conn_id = postgres_conn_id
        self.transform_function = transform_function
        self.file_path = file_path
        self.abs_file_path = None

    def execute(self, context):
        """Implementation of the Operator execute() method."""
        #### Postgres SELECT query block
        try:
            # Init Airflow Postgres Hook
            pg = PostgresHook(postgres_conn_id=self.postgres_conn_id)
            # Get records via an SQL query
            # with open(self.sql) as sql_file: sql = sql_file.read()
            records = pg.get_records(sql=self.sql)
        # Raise block exception        
        except: raise
        #### Transformations block
        try:
            # Apply transformation function
            results = self.transform_function(records)
        # Raise block exception 
        except: raise    
        #### JSON export block
        try:
            # Get file absolute path
            self.abs_file_path = get_absolute_path(self.file_path, context)
            # Export as JSON file
            with open(self.abs_file_path, "w") as json_file:
                json.dump(results, json_file, indent="4")
        # Raise block exception        
        except: raise