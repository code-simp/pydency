"""
This file has the code to list all the dependencies of your python application
"""

# Importing Dependencies
from src.error_types import (
    FileNotFoundError
)

from src.config_api import (
    get_config_api
)

from typing import (
    Any
)


import os


# Singleton cfg
cfg = get_config_api()


class DependencyGetter:

    """
    The main class that does the manual labor to fetch application only dependencies of a python module

    import patterns covered:
    
    1. import a
    2. from a import b
    3. from a.b import c

    """

    POSSIBLE_IMPORT_PATTERNS = {
        r'^import (.*)',
        r'^from (.*) import (.*)',
        r'^from (.*)\.+(.*) import (.*)'
    }


    def _read_file_contents(self, file_to_read, encoding_to_read_with=cfg.DEFAULT_READ_ENCODING):

        """
        The name says it all, just reads stuff
        """

        if not os.path.exists(file_to_read):
            raise FileNotFoundError

        return open(file_to_read, encoding=encoding_to_read_with).readlines()

    def _get_possible_import_patterns_for_line():
        pass


    def _get_dependency(self, file_name_to_look_for):

        """
        The heavy lifter that does the extraction of modules
        """
        
        visited_files = set()
        files_to_visit = []
        
        while files_to_visit:
            file_to_visit = files_to_visit.pop()
            file_lines = self._read_file_contents(files_to_visit)
            
            for line in file_lines:
                pass
