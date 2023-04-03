"""
This module contains validate and parse functions that are used by the pyTaskify.
"""

import sys

def validate_task_type(task_name, tasks_config):
    """
    Validates if the task type is valid.

    :param task_name: The name of the task to be validated.
    :param tasks_config: The configuration containing the tasks.

    :return: None

    :raises: SystemExit if the task is not valid.
    """
    task = tasks_config.get(task_name)

    if not task:
        print(f"The task '{task_name}' does not exist.")
        sys.exit(1)

    task_types = ["cmd", "cmds", "task", "tasks"]
    num_task_types = sum(key in task for key in task_types)
    if num_task_types == 0:
        print(f"The task '{task_name}' does not have a command, list of commands, or another task.")
        sys.exit(1)
    elif num_task_types > 1:
        print(f"The task '{task_name}' has more than one type of command (cmd, cmds, task, tasks).")
        sys.exit(1)


def parse_task_args(task_args, user_args):
    """
    Parses the task arguments.

    :param task_args: The dictionary containing the task arguments.
    :param user_args: The list containing the arguments passed by the user.

    :return: A dictionary containing the parsed task arguments.

    :raises: SystemExit if any argument is invalid or required argument is not passed.
    """
    parsed_args = {}
    provided_args = {}

    # Map each alias to the corresponding argument name
    aliases = {}
    for arg_name, arg_value in task_args.items():
        alias_list = arg_value.get('alias')
        if not isinstance(alias_list, list):
            alias_list = [alias_list]
        for alias in alias_list:
            if alias in aliases:
                print(f"The alias '{alias}' is being used for more than one argument.")
                sys.exit(1)
            aliases[alias] = arg_name

    if isinstance(user_args, dict):
        # Transform the dictionary of arguments into a list
        user_args_list = []
        for arg_name, arg_value in user_args.items():
            user_args_list.append(f"{arg_name}")
            user_args_list.append(f"{arg_value}")
        user_args = user_args_list

    # Verify if the argument is valid
    valid_args = list(aliases.keys()) + list(task_args.keys())
    for arg_name in user_args[::2]:
        if arg_name not in valid_args:
            print(f"The argument '{arg_name}' is not valid.")
            sys.exit(1)

    # Iterate over the user provided arguments
    index_arg = 0

    while index_arg < len(user_args):
        user_arg = user_args[index_arg]
        index_arg += 1

        # Check if argument has already been provided before, with the same name or a different alias
        arg_name = aliases.get(user_arg, user_arg)
        if arg_name in provided_args:
            print(f"The argument '{arg_name}' has already been provided before.")
            sys.exit(1)
        provided_args[arg_name] = True

        # Get argument name if is an alias
        arg_name = aliases.get(user_arg, arg_name)

        # Check if argument is a flag
        if task_args[arg_name].get('is_flag'):
            parsed_args[arg_name] = True
        else:
            # Parse argument value
            arg_value = user_args[index_arg] if index_arg < len(user_args) else None
            if arg_value is None:
                if task_args[arg_name].get('required'):
                    print(f"The argument '{task_args[arg_name]['alias']}' is required.")
                    sys.exit(1)
                elif 'default' in task_args[arg_name]:
                    parsed_args[arg_name] = task_args[arg_name]['default']
                else:
                    parsed_args[arg_name] = ''
            else:
                parsed_args[arg_name] = arg_value
                index_arg += 1

    # Check if any required argument is missing
    for arg_name, arg_value in task_args.items():
        if arg_value.get('required') and arg_name not in parsed_args:
            print(f"The argument '{task_args[arg_name]['alias']}' is required.")
            sys.exit(1)

    # Check if any optional argument is missing and set its value to None or default value
    for arg_name, arg_value in task_args.items():
        if not arg_value.get('required') and arg_name not in parsed_args:
            parsed_args[arg_name] = arg_value.get('default', '')

    return parsed_args
