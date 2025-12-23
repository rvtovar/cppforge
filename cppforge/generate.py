import json
import os
import subprocess
import sys
from pathlib import Path


def find_cmake_presets(json_path: str, preset_name: str) -> dict:
    """
    Parse CMakePresets.json to find the requested preset configuration.
    """
    # Check if the JSON file exists
    if not Path(json_path).is_file():
        print(f"Error: {json_path} not found!")
        sys.exit(1)

    # Load the JSON file
    with open(json_path, "r") as f:
        cmake_presets = json.load(f)

    # Check for presets in the file
    presets = cmake_presets.get("presets", cmake_presets.get("configurePresets", []))
    for preset in presets:
        if preset["name"] == preset_name:
            return preset

    print(f"Error: Preset '{preset_name}' not found in {json_path}.")
    sys.exit(1)

def generate_and_build(preset_name: str, export_compile_commands: bool):
    """
    Generate the build configuration using a CMake preset and optionally export compile commands.
    Use the generator specified in the preset to build the project.
    """
    import shutil

    # Define the path to CMakePresets.json
    json_path = "CMakePresets.json"

    # Find the appropriate preset
    preset = find_cmake_presets(json_path, preset_name)

    # Retrieve the build directory from the preset
    build_dir = preset.get("buildDir", "build")

    # Ensure the build directory exists
    Path(build_dir).mkdir(parents=True, exist_ok=True)

    # Build the base CMake command
    preset_command = [
        "cmake",
        f"--preset={preset_name}"
    ]

    # Optionally add the compile commands flag
    if export_compile_commands:
        print("Enabling export of compile commands...")
        preset_command.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=ON")

    # Run the CMake configuration step
    print(f"Running CMake with preset '{preset_name}'...")
    subprocess.run(preset_command, check=True)

    # Determine the generator from the preset (e.g., Ninja, Makefiles)
    generator = preset.get("generator", "Ninja").lower()

    # Build the project using the detected generator
    if generator == "ninja":
        print("Building project with Ninja...")
        build_command = ["ninja", "-C", build_dir]
    elif "make" in generator:
        print("Building project with Makefiles...")
        build_command = ["make", "-C", build_dir]
    else:
        raise ValueError(f"Unsupported generator '{preset.get('generator')}'. Please use Ninja or Makefiles.")

    # Execute the build command
    subprocess.run(build_command, check=True)

    print("Generate and build complete!")


def extract_project_name(cmake_file_path: str) -> str:
    """
    Extract the project name from a CMakeLists.txt file.

    Args:
        cmake_file_path (str): Path to the CMakeLists.txt file.

    Returns:
        str: The name of the project.

    Raises:
        ValueError: If the project name cannot be found in the CMakeLists.txt file.
    """
    project_line_prefix = "project("
    with open(cmake_file_path, "r") as cmake_file:
        for line in cmake_file:
            line = line.strip()
            if line.lower().startswith(project_line_prefix):
                # Extract the project name between parentheses
                name = line[len(project_line_prefix):].split(")")[0].strip()
                if name:
                    p1 = name.split()
                    p2 = p1[0].split("/")
                    return p2[0]
    raise ValueError("Could not find a valid project name in CMakeLists.txt.")


def read_preset_data(json_path: str, preset_name: str) -> dict:
    """
    Read the configurePreset details from CMakePresets.json.

    Args:
        json_path (str): Path to the CMakePresets.json file.
        preset_name (str): Name of the configure preset.

    Returns:
        dict: The preset details (including `generator` and `binaryDir`).

    Raises:
        ValueError: If the preset or the JSON file is invalid.
    """
    import json

    # Check if the JSON file exists
    if not Path(json_path).is_file():
        raise FileNotFoundError(f"{json_path} not found.")

    # Load and parse the JSON file
    with open(json_path, "r") as f:
        cmake_data = json.load(f)

    # Locate the specified preset
    presets = cmake_data.get("configurePresets", [])
    for preset in presets:
        if preset.get("name") == preset_name:
            return preset
    
    # Raise error if the preset isn't found
    raise ValueError(f"Preset '{preset_name}' not found in {json_path}.")


def build_and_run(preset_name: str, executable: str = None):
    """
    Build the project using the generator and binaryDir from CMakePresets.json, then run the target executable.

    Args:
        preset_name (str): The CMake configure preset name.
        executable (str): Optional. Path to the executable to run. If not specified,
                          the project name from CMakeLists.txt will be used.
    """
    # Path to CMakePresets.json
    json_path = "CMakePresets.json"

    # Read the preset data (including generator and binaryDir)
    try:
        preset_data = read_preset_data(json_path, preset_name)
        generator = preset_data.get("generator", "Ninja").lower()
        build_dir = preset_data.get("binaryDir", "build")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    print(f"Using generator '{generator}' and build directory '{build_dir}' from preset '{preset_name}'.")

    # Validate the build directory
    build_path = Path(build_dir)
    if not build_path.exists():
        print(f"Error: Build directory '{build_dir}' does not exist. Please generate the project first.")
        return

    # Build the project with the detected generator
    if "ninja" in generator:
        build_command = ["ninja", "-C", build_dir]
    elif "make" in generator:
        build_command = ["make", "-C", build_dir]
    else:
        print(f"Error: Unsupported generator '{generator}'. Only Ninja and Makefiles are supported.")
        return

    print(f"Building project with {generator}...")
    subprocess.run(build_command, check=True)

    # Determine executable name if not explicitly provided
    if not executable:
        print("No executable provided. Inferring from CMakeLists.txt...")
        cmake_file_path = Path("CMakeLists.txt")
        if not cmake_file_path.exists():
            print("Error: CMakeLists.txt not found in the current directory.")
            return

        # Extract the project name from CMakeLists.txt
        try:
            project_name = extract_project_name(str(cmake_file_path))
            executable = str(build_path / project_name)
        except ValueError as e:
            print(f"Error: {e}")
            return

    # Validate the executable
    if not Path(executable).is_file():
        print(f"Error: Executable '{executable}' does not exist. Did the build succeed?")
        return

    # Run the executable
    print(f"Running target executable: {executable}...")

    print("\n\n\n")
    subprocess.run([executable])

def build(preset_name: str):
    """
    Build the project using the generator and binaryDir from CMakePresets.json

    Args:
        preset_name (str): The CMake configure preset name.
    """
    # Path to CMakePresets.json
    json_path = "CMakePresets.json"

    # Read the preset data (including generator and binaryDir)
    try:
        preset_data = read_preset_data(json_path, preset_name)
        generator = preset_data.get("generator", "Ninja").lower()
        build_dir = preset_data.get("binaryDir", "build")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    print(f"Using generator '{generator}' and build directory '{build_dir}' from preset '{preset_name}'.")

    # Validate the build directory
    build_path = Path(build_dir)
    if not build_path.exists():
        print(f"Error: Build directory '{build_dir}' does not exist. Please generate the project first.")
        return

    # Build the project with the detected generator
    if "ninja" in generator:
        build_command = ["ninja", "-C", build_dir]
    elif "make" in generator:
        build_command = ["make", "-C", build_dir]
    else:
        print(f"Error: Unsupported generator '{generator}'. Only Ninja and Makefiles are supported.")
        return

    print(f"Building project with {generator}...")
    subprocess.run(build_command, check=True)

   
def run(preset_name: str, executable: str = None):
    """
    Runs the Project

    Args:
        preset_name (str): The CMake configure preset name.
        executable (str): Optional. Path to the executable to run. If not specified,
                          the project name from CMakeLists.txt will be used.
    """
     # Path to CMakePresets.json
    json_path = "CMakePresets.json"

    # Read the preset data (including generator and binaryDir)
    try:
        preset_data = read_preset_data(json_path, preset_name)
        build_dir = preset_data.get("binaryDir", "build")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return


    # Validate the build directory
    build_path = Path(build_dir)
    if not build_path.exists():
        print(f"Error: Build directory '{build_dir}' does not exist. Please generate the project first.")
        return

    # Determine executable name if not explicitly provided
    if not executable:
        print("No executable provided. Inferring from CMakeLists.txt...")
        cmake_file_path = Path("CMakeLists.txt")
        if not cmake_file_path.exists():
            print("Error: CMakeLists.txt not found in the current directory.")
            return

        # Extract the project name from CMakeLists.txt
        try:
            project_name = extract_project_name(str(cmake_file_path))
            executable = str(build_path / project_name)
        except ValueError as e:
            print(f"Error: {e}")
            return

    # Validate the executable
    if not Path(executable).is_file():
        print(f"Error: Executable '{executable}' does not exist. Did the build succeed?")
        return

    # Run the executable
    print(f"Running target executable: {executable}...")

    print("\n\n\n")
    subprocess.run([executable])


