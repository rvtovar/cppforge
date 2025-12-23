from pathlib import Path
import json
import subprocess
from cppforge.colors import print_error, print_success, print_info, print_warning


def find_cmake_presets(json_path: str, preset_name: str) -> dict:
    """
    Parse CMakePresets.json to find the requested preset configuration.
    """
    # Check if the JSON file exists
    if not Path(json_path).is_file():
        print_error(f"The file '{json_path}' was not found.")
        raise FileNotFoundError(f"{json_path} not found.")

    # Load the JSON file
    with open(json_path, "r") as f:
        cmake_presets = json.load(f)

    # Check for presets in the file
    presets = cmake_presets.get("presets", cmake_presets.get("configurePresets", []))
    for preset in presets:
        if preset["name"] == preset_name:
            return preset

    print_error(f"Preset '{preset_name}' not found in {json_path}.")
    raise ValueError(f"Preset '{preset_name}' not found.")


def generate_and_build(preset_name: str, export_compile_commands: bool):
    """
    Generate the build configuration using a CMake preset and optionally export compile commands.
    Use the generator specified in the preset to build the project.
    """
    # Define the path to CMakePresets.json
    json_path = "CMakePresets.json"

    # Find the appropriate preset
    preset = find_cmake_presets(json_path, preset_name)

    # Retrieve the build directory from the preset
    build_dir = preset.get("buildDir", "build")

    # Ensure the build directory exists
    Path(build_dir).mkdir(parents=True, exist_ok=True)

    # Build the base CMake command
    preset_command = ["cmake", f"--preset={preset_name}"]

    # Optionally add the compile commands flag
    if export_compile_commands:
        print_info("Enabling export of compile commands...")
        preset_command.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=ON")

    # Run the CMake configuration step
    print_info(f"Running CMake with preset '{preset_name}'...")
    subprocess.run(preset_command, check=True)

    # Build the project
    build(preset_name)

    print_success("Generate and build complete!")


def build(preset_name: str):
    """
    Build the project using the generator and binaryDir from CMakePresets.json.

    Args:
        preset_name (str): The CMake configure preset name.
    """
    # Path to CMakePresets.json
    json_path = "CMakePresets.json"

    # Read the preset data (including generator and binaryDir)
    try:
        preset_data = find_cmake_presets(json_path, preset_name)
        generator = preset_data.get("generator", "Ninja").lower()
        build_dir = preset_data.get("binaryDir", "build")
    except (FileNotFoundError, ValueError) as e:
        print_error(str(e))
        return

    print_info(f"Using generator '{generator}' and build directory '{build_dir}' from preset '{preset_name}'.")

    # Validate the build directory
    build_path = Path(build_dir)
    if not build_path.exists():
        print_error(f"Build directory '{build_dir}' does not exist. Please generate the project first.")
        return

    # Build the project with the detected generator
    if "ninja" in generator:
        build_command = ["ninja", "-C", build_dir]
    elif "make" in generator:
        build_command = ["make", "-C", build_dir]
    else:
        print_error(f"Unsupported generator '{generator}'. Only Ninja and Makefiles are supported.")
        return

    print_info(f"Building project with {generator}...")
    subprocess.run(build_command, check=True)
    print_success("Build completed successfully.")


def run(preset_name: str, executable: str = None):
    """
    Run the project based on the CMake preset.

    Args:
        preset_name (str): The CMake configure preset name.
        executable (str): Optional. Path to the executable to run. If not specified,
                          the project name from CMakeLists.txt will be used.
    """
    json_path = "CMakePresets.json"

    # Read the preset data (including binaryDir)
    try:
        preset_data = find_cmake_presets(json_path, preset_name)
        build_dir = preset_data.get("binaryDir", "build")
    except (FileNotFoundError, ValueError) as e:
        print_error(str(e))
        return

    # Validate the build directory
    build_path = Path(build_dir)
    if not build_path.exists():
        print_error(f"Build directory '{build_dir}' does not exist. Please generate the project first.")
        return

    # Determine executable name if not explicitly provided
    if not executable:
        print_info("No executable provided. Inferring from CMakeLists.txt...")
        cmake_file_path = Path("CMakeLists.txt")
        if not cmake_file_path.exists():
            print_error("CMakeLists.txt not found in the current directory.")
            return

        # Extract the project name from CMakeLists.txt
        try:
            executable = extract_project_name(str(cmake_file_path))
            executable = str(build_path / executable)
        except ValueError as e:
            print_error(str(e))
            return

    # Validate the executable
    if not Path(executable).is_file():
        print_error(f"Executable '{executable}' does not exist. Did the build succeed?")
        return

    # Run the executable
    print_info(f"Running target executable: {executable}...")
    print("\n" * 3)
    subprocess.run([executable])


def build_and_run(preset_name: str, executable: str = None):
    """
    Build and then run the project using the specified preset.
    """
    print_info(f"Building project using preset '{preset_name}'...")
    build(preset_name)
    print_info("Build step completed.")
    print_info("Running the project...")
    run(preset_name, executable)


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
                p1 = name.split()
                p2 = p1[0].split("/")
                return p2[0]
    raise ValueError("Could not find a valid project name in CMakeLists.txt.")
