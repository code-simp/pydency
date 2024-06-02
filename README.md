# pydency
A python library that lists the application-only-dependencies of a single python module


# Usage

1. Command line way of invoking

pydency <file_name>

You need to run this command from the root of the application


2. Programmatic way of invoking

from pydency import get_dependencies
dependencies_list = get_dependencies(root_path_of_the_application, file_name) -> returns a list of <str> dependency module names


# Note

The library is still under development and currently supported fetching dependencies for following imports patterns

1. import a
2. from a import b
3. from a import b, c
4. from a.b import c
5. from a.b import c, d