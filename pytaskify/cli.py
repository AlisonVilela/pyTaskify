"""
This module contains helper functions that are used by the pyTaskify CLI.
"""

import sys
from pytaskify.helpers import print_help, print_version, list_all
from pytaskify.config import load_config
from pytaskify.executor import execute_task
from pytaskify.tasks import parse_task_args

def main():
    """The entry point of the pyTaskify CLI."""
    args = sys.argv[1:]

    # If no arguments are passed, display help
    if not args:
        print_help()
        sys.exit()

    # Handle passed arguments
    if '-h' in args or '--help' in args:
        print_help()
        sys.exit()

    if '-v' in args or '--version' in args:
        print_version()
        sys.exit()

    # Load configuration from taskify.yml file
    try:
        config = load_config('taskify.yml')
    except FileNotFoundError:
        print('File taskify.yml not found.')
        sys.exit(1)

    current_config = config
    index_arg = 0

    while index_arg < len(args):
        arg = args[index_arg]
        module_names = current_config.get("modules", {}).keys()

        if arg in module_names:
            current_config = current_config[arg]
            index_arg += 1
        elif arg in current_config.get("tasks", {}):
            task_name = arg
            task_args = current_config["tasks"][task_name].get("args", {})
            parsed_args = parse_task_args(task_args, args[index_arg+1:])
            execute_task(task_name, current_config["tasks"], parsed_args, config["work_dir"])
            sys.exit()
        elif arg in ["-l", "--list"]:
            list_all(current_config)
            sys.exit()
        else:
            print(f"{arg} is not a valid module or task.")
            sys.exit(1)

    # If no remaining positional arguments, display help
    print_help()
    sys.exit()

if __name__ == '__main__':
    main()
