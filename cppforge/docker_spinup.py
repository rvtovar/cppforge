import os
import subprocess
import sys
from pathlib import Path
import shutil

def spinup(compose_file: str, container_name: str = "gcc-clang-dev") -> None:
    """Spin up a dev container, exec into it, and clean up on exit."""

    # Colors for terminal output
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    NC = "\033[0m"  # No color

    # Ensure Docker is installed
    if not shutil.which("docker"):
        print(f"{RED}Error: Docker is not installed or not in PATH.{NC}")
        sys.exit(1)
    
    # Ensure Docker Compose is installed
    try:
        subprocess.run(
            ["docker", "compose", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError:
        print(f"{RED}Error: Docker Compose is not installed or not working.{NC}")
        sys.exit(1)

    # Check if compose file exists
    if not Path(compose_file).is_file():
        print(f"{RED}Error: Compose file '{compose_file}' does not exist!{NC}")
        sys.exit(1)

    try:
        # Get the project directory (working directory)
        project_dir = os.getcwd()
        print(f"{GREEN}Using project directory: {project_dir}{NC}")
        print(f"{YELLOW}Starting Docker Compose...{NC}")

        # Start the container
        subprocess.run(
            ["docker", "compose", "-f", compose_file, "up", "-d", "dev"],
            env={**os.environ, "PROJECT_DIR": project_dir},
            check=True,
        )
        print(f"{GREEN}Container started successfully.{NC}")

        # Exec into the running container shell
        print(f"{YELLOW}Entering the Docker container shell... Exit to stop the container.{NC}")
        subprocess.run(
            ["docker", "exec", "-it", container_name, "zsh"],
            check=True,
        )

    except KeyboardInterrupt:
        print(f"{RED}\nCaught KeyboardInterrupt. Cleaning up...{NC}")
    finally:
        # Whether exiting the shell or hitting CTRL+C, bring down the container
        print(f"{RED}Bringing down Docker Compose...{NC}")
        subprocess.run(["docker", "compose", "-f", compose_file, "down"], check=False)
        print(f"{GREEN}Cleanup complete.{NC}")
