"""
This file has the code to list all the dependencies of your python application
"""

# Importing Dependencies
from src.error_types import FileNotFoundError

import os


def read_file_contents(file_to_read, encoding_to_read_with=DEFAULT_READ_ENCODING):

    if not os.path.exists(file_to_read):
        raise FileNotFoundError

    return open(file_to_read, encoding=encoding_to_read_with).readlines()


def _get_dependency(file_name_to_look_for):
    
    visited_files = set()
    files_to_visit = []
    
    while files_to_visit:
        file_to_visit = files_to_visit.pop()
        file_lines = read_file_contents(files_to_visit)