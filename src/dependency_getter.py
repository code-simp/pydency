"""
This file has the code to list all the dependencies of your python application
"""

# Importing Dependencies
from .error_types import (
    FileNotFoundError
)

from .config_api import (
    get_config_api
)

from typing import (
    Any
)

import re
import os


# Singleton cfg
cfg = get_config_api()


class DependencyGetter:

    """
    The main class that does the manual labor to fetch application only dependencies of a python module

    import patterns covered:
    
    1. import a
    2. from a import b
    3. from a import b, c
    4. from a.b import c
    5. from a.b import c, d

    """

    def __init__(self, application_path):
        self.application_path = application_path


    POSSIBLE_IMPORT_PATTERNS = {
        r'^import (.*)',
        r'^from (.*) import (.*)',
        r'^from (.*)\.+(.*) import (.*)'
    }

    def _read_file_contents(self, file_to_read, encoding_to_read_with=cfg.DEFAULT_READ_ENCODING):

        """
        The name says it all, just reads stuff
        """

        if not os.path.exists(os.path.join(self.application_path, file_to_read)):
            raise FileNotFoundError

        return open(os.path.join(self.application_path, file_to_read), encoding=encoding_to_read_with).readlines()

    def _parse_pattern_found(self, pattern):

        """
        Given a pattern found in code, parses if any characters like "," found in it
        """

        delimiters = [',', '.']
        
        for delimiter in delimiters:
            if delimiter in pattern:
                return tuple([pat.strip() for pat in pattern.split(delimiter)])
        return pattern

    def _get_possible_import_patterns_for_line(self, input_line):

        """
        given a line, returns a list of tuples where each tuple has multiple module names
        
        NOTE: currently assumes that there can only be one pattern in a line

        PARAM: input_line -> str

        RETURN: 
        -> [(X, Y), (X, Y, Z)]
        -> in case where RHS has ',' seperated values there can be nested tuples [(X, (Y, Z))]
        """
        
        import_results = []

        for search_pattern in self.POSSIBLE_IMPORT_PATTERNS:
            pattern_result = re.findall(search_pattern, input_line)
            if pattern_result:
                if isinstance(pattern_result[0], tuple):
                    pattern_result = pattern_result[0]
                for pattern in pattern_result:

                    # 1. if "." in pattern
                    if '.' in pattern:
                        for inner_pattern in self._parse_pattern_found(pattern):
                            import_results.append(inner_pattern)
                        continue

                    # 2. if ',' delimiter found
                    import_results.append(
                        self._parse_pattern_found(
                            pattern
                        )
                    )
                break
        return import_results

    def _get_possible_files(self, import_patterns):
        
        """
        given a patterns list, tries to find possible patterns for that combination of patterns
        """

        def _test_and_return_verified_path(pos_path):
            if os.path.exists(pos_path):
                return pos_path
            return ''

        verified_paths = set()
        possible_path = self.application_path

        # CASE 1:
        if len(import_patterns) == 1:
            possible_path = os.path.join(possible_path, import_patterns[0] + cfg.PY_EXTENSION)
            return _test_and_return_verified_path(possible_path)

        # CASE 2, 3, 4, 5
        for pattern in import_patterns:
            if isinstance(pattern, str):
                possible_path = os.path.join(possible_path, pattern)
            elif isinstance(pattern, tuple) or isinstance(pattern, list):
                current_possible_path = possible_path
                for inner_pattern in pattern:
                    possible_path = os.path.join(possible_path, inner_pattern + cfg.PY_EXTENSION)
                    verified_path = _test_and_return_verified_path(possible_path)
                    if verified_path:
                        verified_paths.add(verified_path)
                possible_path = current_possible_path
        
        # case 2, 4
        if possible_path:
            verified_path = _test_and_return_verified_path(possible_path + cfg.PY_EXTENSION)
            if verified_path:
                verified_paths.add(verified_path)
        
        return list(verified_paths)
        


    def _get_dependency(self, file_name_to_look_for):

        """
        The heavy lifter that does the extraction of modules
        """
        
        visited_files = {}
        files_to_visit = [file_name_to_look_for, ]
        
        while files_to_visit:
            file_to_visit = files_to_visit.pop()
            visited_files.add(file_to_visit)
            file_lines = self._read_file_contents(file_to_visit)
            
            for line in file_lines:
                import_patterns = self._get_possible_import_patterns_for_line(line)
                possible_files = self._get_possible_files(import_patterns)

                if possible_files:
                    for file in possible_files:
                        if file not in visited_files:
                            files_to_visit.append(file)
        
        return list(visited_files)

    def get_dependency(self, file_name_to_look_for):
        self._get_dependency(file_name_to_look_for=file_name_to_look_for)
