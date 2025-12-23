from jinja2 import Template
import os
from cppforge.colors import print_info, print_error, print_success


def create_class(name, header_template="../templates/class.hpp.template", impl_template="../templates/class.cpp.template"):
    """
    Generate a new class with both a header and implementation file.

    Args:
        name (str): The name of the class.
        header_template (str): Path to the .hpp template file.
        impl_template (str): Path to the .cpp template file.
    """
    try:
        # Ensure the include and src directories exist
        os.makedirs("include", exist_ok=True)
        os.makedirs("src", exist_ok=True)

        # Paths for the output files
        header_path = f"include/{name}.hpp"
        implementation_path = f"src/{name}.cpp"

        # ------------------------------------ #
        # Process the header template
        # ------------------------------------ #
        try:
            print_info(f"Loading header template: {header_template}")
            with open(header_template, "r") as header_file:
                header_template_content = Template(header_file.read())
            header_content = header_template_content.render(ClassName=name)

            with open(header_path, "w") as header_output:
                header_output.write(header_content)

            print_success(f"Created header: {header_path}")
        except FileNotFoundError:
            print_error(f"Header template file not found: {header_template}")
            return
        except Exception as e:
            print_error(f"An error occurred while processing the header template: {e}")
            return

        # ------------------------------------ #
        # Process the implementation template
        # ------------------------------------ #
        try:
            print_info(f"Loading implementation template: {impl_template}")
            with open(impl_template, "r") as impl_file:
                impl_template_content = Template(impl_file.read())
            impl_content = impl_template_content.render(ClassName=name)

            with open(implementation_path, "w") as impl_output:
                impl_output.write(impl_content)

            print_success(f"Created implementation: {implementation_path}")
        except FileNotFoundError:
            print_error(f"Implementation template file not found: {impl_template}")
            return
        except Exception as e:
            print_error(f"An error occurred while processing the implementation template: {e}")
            return

    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
