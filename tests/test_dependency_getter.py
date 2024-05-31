"""
A pytest based unittests for src/dependency_getter.py
"""

from ..src import dependency_getter

import os


dep_getter = dependency_getter.DependencyGetter(os.getcwd())


def test_parse_pattern_found():
    assert dep_getter._parse_pattern_found('dummy_lib') == 'dummy_lib'
    assert dep_getter._parse_pattern_found(' dummy_lib1.dummy_lib2 ') == ('dummy_lib1', 'dummy_lib2')
    assert dep_getter._parse_pattern_found(' dummy_lib1, dummy_lib2 ') == ('dummy_lib1', 'dummy_lib2')

def test_get_possible_import_patterns_for_line():
    assert dep_getter._get_possible_import_patterns_for_line('import abc') == ['abc']
    assert dep_getter._get_possible_import_patterns_for_line('from abc import xyz') == ['abc', 'xyz']
    assert dep_getter._get_possible_import_patterns_for_line('from abc import x, y') == ['abc', ('x', 'y')]
    assert dep_getter._get_possible_import_patterns_for_line('from abc.xyz import p') == ['abc', 'xyz', 'p']
    assert dep_getter._get_possible_import_patterns_for_line('from abc.xyz import p, q') == ['abc', 'xyz', ('p', 'q')]

def test_get_dependency():
    pass
