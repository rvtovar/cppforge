from jinja2 import Template
import os

def create_new_module(name, template_path="../templates/module.ixx.template"):
    """
    Generate a new module file from a template.

    Args:
        name (str): Name of the module.
        template_path (str): Path to the template file.
    """
    # Ensure the `src` directory exists
    os.makedirs("src", exist_ok=True)

    # Path for the new module file
    module_path = f"src/{name}.ixx"

    try:
        # Read the module template
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())  # Load the Jinja2 template

        # Render the template with the provided module name
        module_content = template.render(ModuleName=name)

        # Write the rendered content to the new module file
        with open(module_path, "w") as module_output:
            module_output.write(module_content)

        print(f"Created new module: {module_path}")
    
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
