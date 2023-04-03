"""
This module contains helper functions that are used by the pyTaskify CLI.
"""

import os
import sys
from pathlib import Path
import yaml

from pytaskify.version import __template__

def load_config(filename):
    """
    Load the YAML configuration file and return a dictionary with the configurations.

    :param filename: Path to the configuration file.
    :return: Dictionary with the configurations from the file.
    """
    config_path = Path(filename)

    # Check if the configuration file exists.
    if not config_path.exists():
        # Try to find a .yaml file if the .yml file is not found.
        if config_path.suffix == '.yml':
            yaml_path = config_path.with_suffix('.yaml')
            if yaml_path.exists():
                config_path = yaml_path
            else:
                print(f"Configuration file '{filename}' not found.")
                sys.exit(1)
        else:
            print(f"Configuration file '{filename}' not found.")
            sys.exit(1)

    # Load the configuration file as a dictionary.
    with config_path.open(encoding='utf8') as file:
        config = yaml.safe_load(file)

    # Check if the 'version' property is present in the configuration file.
    if 'version' not in config:
        print(f"Configuration file '{filename}' does not have the 'version' property.")
        sys.exit(1)

    # Check if the configuration file version is supported.
    if config['version'] != __template__:
        print(f"Configuration file '{filename}' has version {config['version']},"
              f" but the supported version is {__template__}.")
        sys.exit(1)

    # Set the working directory as the directory of the configuration file.
    config['work_dir'] = os.path.dirname(os.path.abspath(config_path))

    # Load module configurations, if any.
    if 'modules' in config:
        for module_name, module_path in config['modules'].items():
            module_file_path = os.path.join(module_path, 'taskify.yml')
            module_config = load_config(module_file_path)
            config[module_name] = module_config

    return config
