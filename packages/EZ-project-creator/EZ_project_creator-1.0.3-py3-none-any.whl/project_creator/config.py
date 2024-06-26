import os
import json

CONFIG_FILE = "project_config.json"


def load_config():
    """Load configuration from the config file.

    Returns:
        dict: Configuration data.
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except json.JSONDecodeError:
        print("Error reading the configuration file. Proceeding with default settings.")
    return {}


def save_config(config):
    """Save configuration to the config file.

    Args:
        config (dict): Configuration data to save.
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except IOError as e:
        print(f"Error saving the configuration file: {e}")
