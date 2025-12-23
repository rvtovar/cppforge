import os
import yaml

DEFAULT_CONFIG = {
    "docker": {
        "docker_compose_file": "docker-compose.yml",  # Default to a local `docker-compose.yml`
        "default_container_name": "gcc-clang-dev",
    },
    "cmake": {
        "presets_path": "CMakePresets.json",
        "default_generator": "Ninja",
    },
}

def load_config():
    """
    Load configuration from `~/.config/cppforge/cppforge.yaml`. Merge it with DEFAULT_CONFIG
    to provide sensible defaults for any missing settings.
    """
    # Define the path to the configuration file
    config_path = os.path.expanduser("~/.config/cppforge/cppforge.yaml")

    # Check if the configuration file exists
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            try:
                user_config = yaml.safe_load(f)  # Load YAML
                # Merge with defaults by recursively overriding
                return merge_dicts(DEFAULT_CONFIG, user_config)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML configuration file: {e}")
                return DEFAULT_CONFIG
    else:
        # Config file doesn't exist, return defaults
        return DEFAULT_CONFIG


def merge_dicts(default, override):
    """
    Recursively merge two dictionaries, prioritizing `override`.
    """
    for key, value in override.items():
        if isinstance(value, dict) and key in default:
            default[key] = merge_dicts(default[key], value)
        else:
            default[key] = value
    return default


def run_setup():
    """
    Create the default configuration for cppforge.
    """
    config_dir = os.path.expanduser("~/.config/cppforge")
    config_file = os.path.join(config_dir, "cppforge.yaml")

    # Create the config directory if it doesn't exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Created configuration directory: {config_dir}")

    # Write the config file if it doesn’t exist
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f)
        print(f"Default configuration created at: {config_file}")
    else:
        print(f"Configuration file already exists at: {config_file}")
