from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from common.utils import get_absolute_path, parse_file, is_int
from dateparser import parse as dateparse
import os
import csv
import json

class FileToPostgresOperator(BaseOperator):
    """
    Airflow Operator that gets data from a file 
    and inserts it in a PostgreSQL database.
    :param file_path: Source file path.
    :param postgres_table: Destination table.
    :param postgres_conn_id: Airflow Connection ID.
    :param file_type: Input file type ("csv" or "json").
        If it's None, the file extension will be considered.
    :param file_delimiter: CSV delimiter value.
    :param transform_id: ID field to transform to int.
        First the ID is casted to int. If this doesn't work then
        a new ID value is generated based on the previous record.
    :param parse_dates: Date fields (list) to parse.
    """
    def __init__(self, file_path, postgres_table, 
                 postgres_conn_id="postgres_default", 
                 file_type=None, file_delimiter=",",
                 transform_id=None, parse_dates=[], 
                 *args, **kwargs):
        # Call super class constructor
        super(FileToPostgresOperator, self).__init__(*args, **kwargs)
        # Set new attributes
        self.file_path = file_path
        self.postgres_table = postgres_table
        self.postgres_conn_id = postgres_conn_id
        self.file_type = file_type
        self.file_delimiter = file_delimiter
        self.transform_id = transform_id
        self.parse_dates = parse_dates
        self.abs_file_path = None

    def execute(self, context):
        """Implementation of the Operator execute() method."""
        #### Input file block
        try:
            # Get file extension, either as an attribute or from the file name
            file_extension = self.file_type or self.file_path.split(".")[-1]
            # Get file absolute path
            self.abs_file_path = get_absolute_path(self.file_path, context)
            # Get rows and fields from file
            rows, fields = parse_file(self.abs_file_path, file_extension, 
                                      self.file_delimiter)
            # ID transformation
            if self.transform_id:
                # Get ID field index 
                id_index = fields.index(self.transform_id)
                # For each row
                for row_index in range(len(rows)):
                    # Get ID value
                    id_ = rows[row_index][id_index]
                    previous_id = rows[row_index-1][id_index]
                    # Transform ID (if it's not an integer)
                    if is_int(id_): rows[row_index][id_index] = int(id_)
                    else: rows[row_index][id_index] = previous_id + 1
            # Date parsing
            if self.parse_dates:
                # For each date field
                for date_field in self.parse_dates:
                    # Get date field index
                    date_index = fields.index(date_field)
                    # Parse date values in each row
                    for row_index in range(len(rows)):
                        date = rows[row_index][date_index]
                        rows[row_index][date_index] = dateparse(date)
        # Raise block exception
        except: raise
        #### Postgres insertion block
        try:
            # Init Airflow Postgres Hook
            pg = PostgresHook(postgres_conn_id=self.postgres_conn_id)
            # Insert rows in Postgres table
            pg.insert_rows(table=self.postgres_table, rows=rows, 
                           target_fields=fields)
        # Raise block exception        
        except: raise
