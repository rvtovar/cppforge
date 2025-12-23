from jinja2 import Template
import os

def create_class_module(module_name, class_name, template_path):
    """
    Generate a basic module class implementation based on a template.

    Args:
        module_name (str): The name of the module (e.g., "PersonModule").
        class_name (str): The name of the class (e.g., "Person").
        template_path (str): The template file path.
    """
    # Ensure the `src` directory exists
    os.makedirs("modules", exist_ok=True)

    # Path for the output module file
    module_file = f"modules/{module_name}.ixx"

    try:
        # Read the template file
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())

        # Render the template with provided variables
        module_content = template.render(ModuleName=module_name, ClassName=class_name)

        # Write the rendered content to the module file
        with open(module_file, "w") as module_output:
            module_output.write(module_content)

        print(f"Created module: {module_file}")
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
