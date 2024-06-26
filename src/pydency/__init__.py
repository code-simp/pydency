
import sys
import os


from pydency.dependency_getter import DependencyGetter

def usage():

    """
    Just a usage method to correct the user
    """

    # Usage section

    print("")
    print("Usage:")
    print("  pydency <file_name>")
    print("")

    # Notes section

    print("Note:")
    print("  you need to run this command from the root of the application")
    print("")
    
    sys.exit(1)


def log_dependencies(file_name, dependencies):
    """
    A uh..uh....beautiful way to print the dependencies ig..
    """
    
    print("")
    print("File:")
    print(f"  {file_name}")
    print("")

    print("Dependencies:")
    if dependencies:
        for dependency_file in dependencies:
            print(f"  {dependency_file}")
    print("")


def get_dependencies(application_path, file_name):

    """
    a simple wrapper to get dependencies
    """

    # the logic
    dep_getter = DependencyGetter(application_path=application_path)
    return dep_getter.get_dependency(file_name)

def main():

    """
    a main-method/script way of calling get_dependencies
    """

    # if file_name arg is missing
    if len(sys.argv) < 2:
        print()
        print("ERROR: Missing file_name argument")
        print()
        usage()

    # required variables
    file_name = sys.argv[1]
    application_path = os.getcwd()

    # fetch the dependencies
    dependencies = get_dependencies(application_path, file_name)
    
    # logging the dependencies
    log_dependencies(file_name, dependencies)
