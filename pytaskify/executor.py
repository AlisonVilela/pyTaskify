"""
This module contains helper functions that are used by the pyTaskify CLI.
"""

import os
import sys
import subprocess
from pytaskify.tasks import parse_task_args, validate_task_type

def run_command(command, work_dir, env, continue_on_error=False, check=False):
    """
    Execute a command in the terminal.

    :param command: The command to execute.
    :param work_dir: The working directory for the command.
    :param env: A dictionary of environment variables.
    :param continue_on_error: If True, continue execution even if the command fails.
    """
    result = subprocess.run(command, shell=True, cwd=work_dir, env=env, check=check)

    if result.returncode != 0:
        if not continue_on_error:
            sys.exit(1)

def execute_task(task_name, tasks_config, parsed_args, work_dir):
    """
    Execute a task with the specified arguments.

    :param task_name: The name of the task to execute.
    :param tasks_config: A dictionary of task configurations.
    :param parsed_args: A dictionary of parsed arguments for the task.
    :param work_dir: The working directory for the task.

    :return: None

    :raises: SystemExit if the task or any subtask is not found, if any argument is invalid,
    if a required argument is not passed, or if a command exits with a non-zero status code.
    """
    validate_task_type(task_name, tasks_config)

    task = tasks_config.get(task_name)

    # Check if the task exists
    if not task:
        print(f"Task '{task_name}' does not exist.")
        sys.exit(1)

    # Execute dependency tasks, if any
    if "deps" in task:
        for dep in task["deps"]:
            execute_task(dep, tasks_config, parsed_args, work_dir)

    continue_on_error = task.get('continue_on_error', False)
    check = task.get('check', False)

    # If there's a single command, execute the command
    if "cmd" in task:
        cmd = str(task["cmd"])
        env = os.environ.copy()

        # Add the environment variables from the configuration, if any
        if 'env' in tasks_config:
            env.update(tasks_config.get("env", {}))

        # Add the environment variables from the task, if any
        if 'env' in task:
            env.update(task.get("env", {}))

        # Replace the placeholders in the command with the parsed arguments
        for arg_name, arg_value in parsed_args.items():
            arg_config = task.get('args', {}).get(arg_name, {})
            if arg_config.get('is_flag'):
                if not arg_value:
                    placeholder = ''
                else:
                    placeholder = arg_config.get('placeholder', '')
            else:
                placeholder = arg_config.get('placeholder', '{value}').replace('{value}', arg_value)
            cmd = cmd.replace("{" + arg_name + "}", placeholder)

        run_command(cmd, env=env, work_dir=work_dir, continue_on_error=continue_on_error, check=check)

     # If there's a list of commands, execute the commands in order
    elif "cmds" in task:
        cmds = task["cmds"]

        for cmd in cmds:
            cmd = str(cmd)
            env = os.environ.copy()

            # Add the environment variables from the configuration, if any
            if 'env' in tasks_config:
                env.update(tasks_config.get("env", {}))

            # Add the environment variables from the task, if any
            if 'env' in task:
                env.update(task.get("env", {}))

            # Replace the placeholders in the command with the parsed arguments
            for arg_name, arg_value in parsed_args.items():
                arg_config = task.get('args', {}).get(arg_name, {})
                if arg_config.get('is_flag'):
                    if not arg_value:
                        placeholder = ''
                    else:
                        placeholder = arg_config.get('placeholder', '')
                else:
                    placeholder = arg_config.get('placeholder', '{value}').replace('{value}', arg_value)
                cmd = cmd.replace("{" + arg_name + "}", placeholder)

            run_command(cmd, env=env, work_dir=work_dir, continue_on_error=continue_on_error, check=check)

    # If there's another task to be executed, execute the task
    elif "task" in task:
        subtask = task["task"]
        subtask_name = subtask
        subtask_args = {}
        parsed_subtask_args = {}
        if isinstance(subtask, dict):
            subtask_name = subtask["name"]
            subtask_args = tasks_config.get(subtask_name).get('args', {})
            parsed_subtask_args = parse_task_args(subtask_args, subtask.get("args", []))
        execute_task(subtask_name, tasks_config, parsed_subtask_args, work_dir)

    # If there's a list of tasks, execute the tasks in order
    elif "tasks" in task:
        subtasks = task["tasks"]

        for subtask in subtasks:
            if isinstance(subtask, str):
                subtask_name = subtask
                subtask_args = {}
            else:
                subtask_name = subtask["name"]
                subtask_args = tasks_config.get(subtask_name).get('args', {})

            # Get the subtask configuration
            subtask_config = tasks_config.get(subtask_name)

            # Check if the subtask exists
            if not subtask_config:
                print(f"Task '{subtask_name}' does not exist.")
                sys.exit(1)

            # Parse the subtask arguments
            parsed_subtask_args = parse_task_args(subtask_args, subtask.get("args", {}))

            # Validate if the required arguments for the subtask have been passed
            for arg_name, arg_config in subtask_args.items():
                if arg_config.get("required") and arg_name not in parsed_subtask_args:
                    print(f"Argument '{arg_name}' is required for the task '{subtask_name}'.")
                    sys.exit(1)

            # Execute the subtask with the passed arguments
            execute_task(subtask_name, tasks_config, parsed_subtask_args, work_dir)
