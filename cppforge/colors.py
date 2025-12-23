# -------------------- Terminal Colors -------------------- #
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No color

def print_error(message):
    """Print an error message in red."""
    print(f"{RED}Error: {message}{NC}")


def print_success(message):
    """Print a success message in green."""
    print(f"{GREEN}{message}{NC}")


def print_info(message):
    """Print an informational message (default color)."""
    print(f"{YELLOW}{message}{NC}")



def print_warning(message):
    """Print a warning message in yellow."""
    print(f"{YELLOW}Warning: {message}{NC}")
