import csv
import json
import os
import ast

def is_int(s):
    """
    Check if a string represents and integer.
    :param s: Input String.
    :return: True or False.
    :rtype: bool
    """
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_absolute_path(file_path, context):
    """
    Get file absolute path using DAG context.
    :param file_path: File path. Can be absolute or relative.
    :param context: DAG context.
    :return: File absolute path.
    :rtype: str
    """
    # Get base path from DAG context
    base_path = os.path.dirname(context["dag"].fileloc)
    # Get file absolute path
    return file_path if os.path.isabs(file_path) \
        else os.path.join(base_path, file_path)

def parse_file(file_path, extension, delimiter):
    """
    Parse file depending on its type (csv, json) 
    and return extracted rows and fields.
    :param file_path: File path.
    :param extension: File extension (csv or json).
    :param delimiter: File delimiter.
    :return: Extracted rows and fields.
    :rtype: (list, list)
    """
    # Init rows and fields
    rows, fields = [], []
    # Open file
    with open(file_path, "r") as file_:
        # CSV file case
        if extension == "csv":
            # Get rows and fields using "csv" library
            csv_reader = list(csv.reader(file_, delimiter=delimiter))
            nb_fields = len(csv_reader[0])
            rows = [row for row in csv_reader if len(row) == nb_fields]
            fields = rows.pop(0)
        # JSON file case
        elif extension == "json":
            # Init dict
            content = {}
            # Get content using "json" library
            try: content = json.load(file_)
            # If "json" fails, use "ast" library
            except: content = ast.literal_eval(file_.read())
            # Get rows and fields from content
            fields = list(json_file[0].keys())
            rows = [[row[field] for field in fields]
                    for row in json_file]
        # Other file types
        else:
            # Raise Type Error
            error = "Invalid file type '{}'.".format(extension)
            raise TypeError(error)
    # Return rows and fields
    return rows, fields