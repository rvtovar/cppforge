#!/usr/bin/env python3
import argparse
import os
from cppforge.class_builder import create_class
from cppforge.module_builder import create_new_module
from cppforge.class_module_builder import create_class_module
from cppforge.new_project import create_new_project
from cppforge.docker_spinup import spinup
from importlib.resources import files

# Helper function for generating a class
def get_templates_path():
    temp_path = files('cppforge').joinpath('templates')
    return temp_path

def is_valid_identifier(name: str) -> bool:
    """
    Check if the provided name is a valid C++ identifier and compatible with CMake/Ninja.
    - Must start with a letter.
    - Can contain letters, numbers, and underscores.
    - Must not be empty.
    """
    if not name:
        return False
    if not name[0].isalpha():
        return False
    if not all(c.isalnum() or c == '_' for c in name):
        return False
    return True

def is_project_directory() -> bool:
    """
    Check if the current directory contains a `CMakeLists.txt` file.
    """
    return os.path.exists('CMakeLists.txt')

def display_help():
    """
    Display help information about available commands.
    """
    print("C++ Project Builder Help")
    print("========================")
    print("Commands:")
    print("  class <class_name> [--m]: Generate a C++ class header file or a module class.")
    print("  module <module_name>: Generates a new module implementation file.")
    print("  new <proj_name> [--prod]: Create a new project.")
    print("  spinup: Spin up a Docker container for development.")
    print("")
    print("Examples:")
    print("  ./script.py class MyClass")
    print("  ./script.py module MyModule")
    print("  ./script.py new MyProject --prod")
    print("  ./script.py spinup")
    print("")
    print("Notes:")
    print("  - Class and module names must be valid C++ identifiers.")
    print("  - Ensure you are in a project directory (has CMakeLists.txt) to run class/module commands.")
    print("  - Use '--help' for this summary.")

def generate_class(name: str):
    """
    Generate an include C++ class header file.
    Args:
        name (str): Class name.
    """
    print(f"Generating class header file for '{name}'...")
    path = get_templates_path()
    header = path / "class.hpp.template"
    impl = path / "class.cpp.template"
    create_class(
        name=name,
        header_template=header,
        impl_template=impl
    )
    print(f"Class '{name}' generated successfully in 'include/{name}.hpp'.")
    print(f"Class '{name}' generated successfully in 'src/{name}.cpp'.")

def generate_module_class(name: str):
    """
    Generate a class that uses modules.
    Args:
        name (str): Class Name.
    """
    path = get_templates_path()
    module = path / "class.ixx.template"
    create_class_module(name, name, module)
    print(f"Generating a class {name} using modules")

def generate_module(module_name: str):
    """
    Generate a C++ module implementation file.
    Args:
        module_name (str): Module name.
    """
    print(f"Generating module file '{module_name}'")
    path = get_templates_path()
    module = path / "module.ixx.template"
    create_new_module(module_name, module)
    print(f"Module '{module_name}' generated successfully in 'src/{module_name}.ixx'.")

def main():
    # Setup Command-Line Argument Parser
    parser = argparse.ArgumentParser(
        description="C++ Project Builder, Class and Module creator, and Docker spinup",
        epilog="Generate C++ classes and modules with ease."
    )

    # Command options
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate Class Command
    class_parser = subparsers.add_parser("class", help="Generate a C++ class header file.")
    class_parser.add_argument("class_name", type=str, help="The name of the class to generate.")
    class_parser.add_argument("--m", action="store_true", help="Make it a module")

    # Generate Module Command
    module_parser = subparsers.add_parser("module", help="Generate a C++ module implementation file.")
    module_parser.add_argument("module_name", type=str, help="The name of the module to generate.")

    # Create A New Project
    proj_parser = subparsers.add_parser("new", help="Generates a new Project")
    proj_parser.add_argument("proj_name", type=str, help="Name of the Project")
    proj_parser.add_argument("--prod", action="store_true", help="Create in Release Mode")

    # Spin Up Docker Container
    docker_parser = subparsers.add_parser("spinup", help="Spinup a docker container")

    # Help Command
    help_parser = subparsers.add_parser("help", help="Show this help message and exit.")

    args = parser.parse_args()

    if args.command == "help":
        display_help()
        return

    # Execute commands based on user input
    if args.command in ("class", "module"):
        if not is_project_directory():
            print("Error: You must be in a project directory (must contain a CMakeLists.txt file) to run this command.")
            return

    if args.command == "class":
        if not is_valid_identifier(args.class_name):
            print(f"Error: Invalid class name '{args.class_name}'. Ensure it starts with a letter and includes only letters, numbers, and underscores.")
            return
        
        if args.m:
            generate_module_class(args.class_name)
        else:
            generate_class(args.class_name)

    elif args.command == "module":
        if not is_valid_identifier(args.module_name):
            print(f"Error: Invalid module name '{args.module_name}'. Ensure it starts with a letter and includes only letters, numbers, and underscores.")
            return
        
        generate_module(args.module_name)

    elif args.command == "new":
        if not is_valid_identifier(args.proj_name):
            print(f"Error: Invalid project name '{args.proj_name}'. Ensure it starts with a letter and includes only letters, numbers, and underscores.")
            return
        
        create_new_project(args.proj_name, prod_mode=args.prod)

    elif args.command == "spinup":
        compose_file = "/home/vanica/Scripts/cpp_cons/docker-compose.yml"
        spinup(compose_file, container_name="gcc-clang-dev")

    print("\nDone. Your files have been generated successfully!")

if __name__ == "__main__":
    main()
