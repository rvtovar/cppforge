from jinja2 import Template
import os

def create_class(name, header_template="../templates/class.hpp.template", impl_template="../templates/class.cpp.template"):
    """
    Generate a new class with both a header and implementation file.

    Args:
        name (str): The name of the class.
        header_template (str): Path to the .hpp template file.
        impl_template (str): Path to the .cpp template file.
    """
    # Ensure the include and src directories exist
    os.makedirs("include", exist_ok=True)
    os.makedirs("src", exist_ok=True)

    # Paths for the output files
    header_path = f"include/{name}.hpp"
    implementation_path = f"src/{name}.cpp"

    try:
        # Read and generate the header file
        with open(header_template, "r") as header_file:
            header_template_content = Template(header_file.read())
        header_content = header_template_content.render(ClassName=name)
        with open(header_path, "w") as header_output:
            header_output.write(header_content)
        print(f"Created header: {header_path}")

        # Read and generate the implementation file
        with open(impl_template, "r") as impl_file:
            impl_template_content = Template(impl_file.read())
        impl_content = impl_template_content.render(ClassName=name)
        with open(implementation_path, "w") as impl_output:
            impl_output.write(impl_content)
        print(f"Created implementation: {implementation_path}")
    
    except FileNotFoundError as e:
        print(f"Error: Template file not found ({e}).")
    except Exception as e:
        print(f"An error occurred: {e}")


