#!/usr/bin/env python3
import argparse
import os
from cppforge.class_builder import create_class
from cppforge.module_builder import create_new_module
from cppforge.class_module_builder import create_class_module
from cppforge.new_project import create_new_project
from cppforge.generate import generate_and_build, build_and_run, build, run
from cppforge.config import run_setup
from cppforge.docker_spinup import spinup
from importlib.resources import files
from pathlib import Path


# -------------------- Utility Functions -------------------- #
def get_templates_path():
    """Get the path to the templates directory."""
    return files('cppforge').joinpath('templates')


def is_valid_identifier(name: str) -> bool:
    """
    Validate the provided identifier for CMake/Ninja compatibility.
    - Must start with a letter.
    - Can contain letters, numbers, and dashes.
    - Must not be empty.
    """
    return name and name[0].isalpha() and all(c.isalnum() or c == '-' for c in name)


def is_project_directory() -> bool:
    """
    Check if the current directory contains a `CMakeLists.txt` file.
    """
    return Path("CMakeLists.txt").is_file()


# -------------------- Command Implementations -------------------- #
def generate_class(name: str):
    """
    Generate a C++ class header and implementation file.
    """
    print(f"Generating class header file for '{name}'...")
    path = get_templates_path()
    create_class(
        name=name,
        header_template=path / "class.hpp.template",
        impl_template=path / "class.cpp.template"
    )
    print(f"Class '{name}' generated successfully in 'include/{name}.hpp' and 'src/{name}.cpp'.")


def generate_module_class(name: str):
    """
    Generate a C++ module-based class.
    """
    print(f"Generating a class '{name}' using modules...")
    path = get_templates_path()
    create_class_module(name, name, path / "class.ixx.template")


def generate_module(module_name: str):
    """
    Generate a C++ module implementation file.
    """
    print(f"Generating module file '{module_name}'...")
    path = get_templates_path()
    create_new_module(module_name, path / "module.ixx.template")
    print(f"Module '{module_name}' generated successfully in 'src/{module_name}.ixx'.")


def configure_parsers(parser):
    """
    Configure the command-line argument parser with subcommands and their arguments.

    Args:
        parser (argparse.ArgumentParser): The main parser object.
    """
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Class Command
    class_parser = subparsers.add_parser("class", help="Generate a C++ class header file.")
    class_parser.add_argument("class_name", type=str, help="The name of the class to generate.")
    class_parser.add_argument("-m", "--module", action="store_true", help="Generate a module-based class.")

    # Module Command
    module_parser = subparsers.add_parser("module", help="Generate a C++ module implementation file.")
    module_parser.add_argument("module_name", type=str, help="The name of the module to generate.")

    # Project Command
    proj_parser = subparsers.add_parser("new", help="Generate a new C++ project.")
    proj_parser.add_argument("proj_name", type=str, help="The name of the project.")
    proj_parser.add_argument("-p", "--prod", action="store_true", help="Create the project in release mode.")

    # Docker Spinup Command
    docker_parser = subparsers.add_parser("spinup", help="Spin up a Docker container for development.")

    # Generate Command
    gen_parser = subparsers.add_parser("generate", help="Generate build configurations using CMakePresets.json.")
    gen_parser.add_argument("-p", "--preset", required=True, help="CMake configure preset to use.")
    gen_parser.add_argument(
        "-e", "--export-compile-commands",
        action="store_true",
        default=True,
        help="Export compile_commands.json during generate process (default: True)"
    )
    gen_parser.add_argument(
        "-n", "--no-export-compile-commands",
        action="store_false",
        dest="export_compile_commands",
        help="Disable export of compile_commands.json."
    )

    # Build and Run Command
    build_run_parser = subparsers.add_parser("build-run", help="Build the project and run the target executable.")
    build_run_parser.add_argument("-p", "--preset", required=True, help="CMake configure preset to use.")
    build_run_parser.add_argument(
        "-e", "--executable",
        default=None,
        help="Optional. Path to the target executable. If not provided, the project name from CMakeLists.txt will be used."
    )

    # Build Command
    build_parser = subparsers.add_parser("build", help="Build the Project.")
    build_parser.add_argument("-p", "--preset", required=True, help="CMake configure preset to use.")

    # Run Command
    run_parser = subparsers.add_parser("run", help="Run the Project.")
    run_parser.add_argument("-p", "--preset", required=True, help="CMake configure preset to use.")
    run_parser.add_argument(
        "-e", "--executable",
        default=None,
        help="Optional. Path to the target executable. If not provided, the project name from CMakeLists.txt will be used."
    )

    subparsers.add_parser("setup", help="Set up default configurations for cppforge")


def main():
    parser = argparse.ArgumentParser(
        description="C++ Project Builder, Class and Module Creator, Build/Run System, and Docker Integration",
        epilog="Generate, build, and run C++ projects with ease."
    )

    # Configure the parsers
    configure_parsers(parser)

    # Parse arguments from the command line
    args = parser.parse_args()

    # Determine which command was called and execute it
    if args.command in ("class", "module"):
        if not is_project_directory():
            print("Error: You must be in a project directory (must contain a CMakeLists.txt file) to run this command.")
            return

    match args.command:

        case "setup":
            run_setup()
        case "class":
            if not is_valid_identifier(args.class_name):
                print(f"Error: Invalid class name '{args.class_name}'. Ensure it starts with a letter and includes only letters, numbers, and dashes.")
                return
            if args.m:
                generate_module_class(args.class_name)
            else:
                generate_class(args.class_name)

        case "module":
            if not is_valid_identifier(args.module_name):
                print(f"Error: Invalid module name '{args.module_name}'. Ensure it starts with a letter and includes only letters, numbers, and dashes.")
                return
            generate_module(args.module_name)

        case "new":
            if not is_valid_identifier(args.proj_name):
                print(f"Error: Invalid project name '{args.proj_name}'. Ensure it starts with a letter and includes only letters, numbers, and dashes.")
                return
            create_new_project(args.proj_name, prod_mode=args.prod)

        case "spinup":
            spinup()

        case "generate":
            generate_and_build(args.preset, args.export_compile_commands)

        case "build-run":
            build_and_run(args.preset, executable=args.executable)

        case "build":
            build(args.preset)
        case "run":
            run(args.preset, executable=args.executable)

if __name__ == "__main__":
    main()
