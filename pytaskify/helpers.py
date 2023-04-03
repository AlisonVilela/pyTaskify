"""
This module contains helper functions that are used by the pyTaskify.
"""

from pytaskify.version import __version__

def print_help():
    """Display the pyTaskify CLI help."""
    help_text = """
pyTaskify - Task runner in Python

Usage:
  pytaskify [options] [module]... [task] [arguments]

Options:
  -l, --list       List available modules and tasks in the current module.
  -h, --help       Display this help message.
  -v, --version    Show pyTaskify version.

Commands:
  module           Navigate through nested modules using module names.
  task             Execute a specific task, providing its name.

Arguments:
  arguments        Optional arguments for a specific task.
"""
    print(help_text)

def print_version():
    """Print the pyTaskify version."""
    print(f'pyTaskify {__version__}')

def list_tasks(config):
    """List the available tasks.

    :param config: The configuration dictionary containing tasks.
    """
    for task_name, task in config.get('tasks', {}).items():
        if 'description' in task:
            print(f"- {task_name}: {task['description']}")
        else:
            print(f"- {task_name}")

def list_modules(config):
    """List the available modules.

    :param config: The configuration dictionary containing modules.
    """
    for module_name in config.get('modules', {}):
        if 'description' in config[module_name]:
            print(f"- {module_name}: {config[module_name]['description']}")
        else:
            print(f"- {module_name}")

def list_all(config):
    """List all available modules and tasks.

    :param config: The configuration dictionary containing modules and tasks.
    """
    if 'description' in config:
        print(config['description'])
        print()

    if len(config.get('modules', {}).items()) > 0:
        print('Available modules:')
        list_modules(config)
        print()

    if len(config.get('tasks', {}).items()) > 0:
        print('Available tasks:')
        list_tasks(config)
        print()
