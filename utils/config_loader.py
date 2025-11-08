import yaml
import os


def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Load configuration settings from a YAML file.

    Args:
        config_path (str): Path to the config.yaml file. 
                           Defaults to "config/config.yaml".

    Returns:
        dict: Parsed configuration as a Python dictionary.
    """
    with open(config_path, "r") as file:
        # Load YAML content into a Python dictionary
        config = yaml.safe_load(file)

    return config
