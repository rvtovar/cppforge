import os
from jinja2 import Template
from importlib.resources import files
from cppforge.config import load_config
import shutil

def copy_cmake_presets(project_dir, temp_path):
    """
    Copy the CMakePresets.json file from the config location to the project directory.

    Args:
        project_dir (str): The directory of the new project.
    """
    config = load_config()
    presets_path = config["cmake"]["presets_path"]  # Path to CMakePresets.json in the config

    # Expand user path and set the destination
    source = os.path.expanduser(presets_path)
    destination = os.path.join(project_dir, "CMakePresets.json")
    
    # Check if the source file exists
    if not os.path.isfile(source):
        print(f"Warning: CMakePresets.json not found at {source}. Using Template.")
        write_file_from_template(temp_path / "CMakePresets.json.template", os.path.join(project_dir, "CMakePresets.json"), context)

        return
    
    try:
        # Copy the file
        shutil.copy(source, destination)
        print(f"Copied CMakePresets.json to {destination}.")
    except Exception as e:
        print(f"Error copying CMakePresets.json: {e}")
def create_new_project(name, prod_mode):
    """Create a new C++23 project using templates."""
    build_type = "Release" if prod_mode else "Debug"
    project_dir = os.path.abspath(name)
    
    # Ensure directory structure
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "include"), exist_ok=True)

    # Utility function for writing rendered content to files
    def write_file_from_template(template_path, output_path, context):
        """Render a Jinja2 template and write the content to a file."""
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
        rendered_content = template.render(context)
        with open(output_path, "w") as output_file:
            output_file.write(rendered_content)
        print(f"Created {output_path}")

    context = {
        "name": name,
        "build_type": build_type,
    }

    def get_templates_path():
        temp_path = files("cppforge").joinpath("templates")
        return temp_path

    temp_path = get_templates_path()
    # Render and write template files
    write_file_from_template(temp_path / "vcpkg.json.template", os.path.join(project_dir, "vcpkg.json"), context)
    write_file_from_template(temp_path / "cmakelist.txt.template", os.path.join(project_dir, "CMakeLists.txt"), context)
    write_file_from_template(temp_path / "main.cpp.template", os.path.join(project_dir, "src/main.cpp"), context)
    write_file_from_template(temp_path / "utilities.ixx.template", os.path.join(project_dir, "src/utilities.ixx"), context)
    write_file_from_template(temp_path / ".clangd.template", os.path.join(project_dir, ".clangd"), context)
    write_file_from_template(temp_path / ".clang-format.template", os.path.join(project_dir, ".clang-format"), context)
    write_file_from_template(temp_path / ".gitignore.template", os.path.join(project_dir, ".gitignore"), context)

    copy_cmake_presets(project_dir, temp_path)


    # Adjust permissions for the bootstrap script
    print(f"Project {name} successfully created in {project_dir}!")
    print("Don't forget to run: vcpkg install to install dependencies.")
