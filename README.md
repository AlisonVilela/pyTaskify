# pyTaskify

A Task Runner written in Python.

`pyTaskify` is a pure Python task runner for automating repetitive tasks in projects.

# Getting started

## Installation

`pyTaskify` is available on `PyPi`. Install the package with

```bash
pip install pytaskify
```

Check that the installation was done correctly by checking the version with the `--version` argument

```bash
taskify --version
```

## Usage

To use `pyTaskify`, execute the `taskify` command with the appropriate arguments. For example, to run the build task:

```bash
taskify build
```

You can also pass arguments to the task. For example, to run the `test` task with the `--verbose` argument:

```bash
taskify test --verbose
```

## Configuration

You can configure `pyTaskify` by creating a `taskify.yml` file in the root directory of your project. This file should contain a list of tasks with their respective configurations.

Here's an example `taskify.yml` file:

```yaml
version: 1

tasks:
    build:
        cmds:
            - rm -rf build
            - mkdir build
            - cd build && cmake .. && make
        env:
            CFLAGS: -O3
            LDFLAGS: -lm
        continue_on_error: true
        check: true
    
    test:
        cmd: ./build/tests --verbose={verbose}
        args:
            verbose:
                is_flag: true
                alias:
                    - -v
                    - --verbose
```

In this example, we have defined two tasks: `build` and `test`.

The `build` task has a list of commands that will be executed in order, and some environment variables that will be set before the commands are run. The `continue_on_error` flag is set to `true`, which means that if one of the commands fails, the remaining commands will still be executed. The `check` flag is set to `true`, which means that if one of the commands fails, the program will exit with a non-zero status code.

The `test` task has a single command, which takes a `verbose` argument. The `args` dictionary defines the `verbose` argument, which is a flag with the `-v` and `--verbose` alias. The `continue_on_error` flag is set to `false`, which means that if the command fails, the program will exit with a non-zero status code. The `check` flag is set to `true`, which means that if the command fails, the program will exit with a non-zero status code.

## Supported file names

`pyTaskify` recognizes a variety of file names that can contain task configurations. These include:

`taskify.yml`

`taskify.yaml`

## Environment variables

You can define environment variables that will be available to all tasks by adding them to the `env` section of the `taskify.yml` file.

```yaml
version: 1

env:
    FOO: bar

tasks:
    default:
        cmd: echo taskify
```

You can also define environment variables for a specific task by adding them to the `env` section of the task configuration.

```yaml
version: 1

tasks:
    default:
        cmd: echo taskify
        env:
            FOO: bar
```

If you use both forms simultaneously, task environment variables will overwrite those previously declared.

```yaml
version: 1

env:
    FOO: bar

tasks:
    default:
        cmd: echo taskify
        env:
            FOO: foobar
```

## Modules

`pyTaskify` lets you import modules and use their functions in your task commands. This can be helpful for organizing your tasks and avoiding code repetition.

```yaml
version: 1

modules:
    foo: ./foo
    bar: ./bar
```

## Tasks Arguments

The `pyTaskify` configuration file allows defining tasks with arguments. Arguments can be used in task commands and can have default values or be marked as required.

These arguments can be used in task commands by using the curly brace syntax `{arg_name}` to reference the argument in the command.

### Properties

A task argument can have the following properties:

- `is_flag` (optional): If set to True, the argument is treated as a flag and does not require a value. Defaults to False.

- `required` (optional): If set to True, the argument is marked as required and must be provided when calling the task. Defaults to False.

- `default` (optional): The default value for the argument. If the argument is not provided, this value will be used instead. If the argument is a flag, the value should be True or False. Defaults to None.

- `alias` (required): A list of aliases for the argument. Aliases can be used in place of the argument name in the task command.

- `placeholder` (optional): The placeholder value for the argument in the task command. This field serves as a mask for the argument, using the `{value}` braces syntax, the argument entry is replaced by the Placeholder and then in the command. Defaults to a string `{value}`.

### Example

```yaml
version: 1

tasks:
    foo:
        cmd: echo foo {verbose}
        args:
            verbose:
                is_flag: true
                placeholder: --verbose
                alias:
                    - -v

    bar:
        cmd: echo bar {color}
        args:
            color:
                placeholder: --color={value}
                default: red
                alias:
                    - -c

    foobar:
        cmd: echo foobar {color} {size}
        args:
            color:
                placeholder: --color={value}
                required: true
                alias:
                    - -c
            size:
                placeholder: --size={value}
                alias:
                    - -s
```

```bash
pytaskify foobar -c blue
pytaskify foobar -c blue -s large
```

```yaml
version: 1

tasks:
  mytask:
    cmd: echo {myarg}
    args:
      myarg:
        required: true
        alias:
          - -m
          - --myarg
        placeholder: --myarg={value}
        default: 'foo'
```

```bash
pytaskify mytask --myarg bar
```

## Tasks Dependencies

You can define dependencies between your tasks with `pyTaskify`. When you run a task, its dependencies will be executed first, if any, the dependency entry is an array.

```yaml
version: 1

tasks:
    build:
        cmd: python build.py

    deploy:
        deps:
            - build
        cmd: python deploy.py ./dist
```

## Tasks Commands and Calling another task

`pyTaskify` lets you define commands for your tasks. These commands can be shell commands, Python scripts, or even other tasks. `pyTaskify` only accepts 1 type of command per task, you must define only 1 between `cmd`, `cmds`, `task` and `tasks`.

```yaml
version: 1

tasks:
    calling_command:
        cmd: echo "Foobar" {FOO}
        args:
            FOO:
                alias: -f

    calling_commands:
        cmds:
            - echo "Step 1"
            - echo "Step 2"

    calling_task:
        task:
            name: calling_command

    calling_tasks:
        tasks:
            - name: calling_command
              args:
                  FOO: bar
```

## Ignore errors

Sometimes it can be useful to ignore errors and continue executing tasks. `pyTaskify` supports this with the `continue_on_error` option.

```yaml
version: 1

tasks:
    calling_commands:
        cmds:
            - echo "Step 1"
            - exit 1
            - echo "Step 3"
        continue_on_error: true
```

## Check errors

If check is true, and the process exits with a non-zero exit code, a CalledProcessError exception will be raised. Attributes of that exception hold the arguments, the exit code, and stdout and stderr if they were captured.

```yaml
version: 1

tasks:
    calling_commands:
        cmds:
            - echo "Step 1"
            - echo "Step 2"
        check: true
```
# Bug Report

Feel free to post an [issue](https://github.com/AlisonVilela/pyTaskify/issues) about any bugs you find, or to ask any questions!

# Contribution

This project uses the Python [subprocess](https://docs.python.org/3/library/subprocess.html) to execute the commands, see the documentation if you need to clarify any doubts!

## Installation

Inside the project folder you can run the command.

```bash
git clone https://github.com/AlisonVilela/pyTaskify.git
cd pyTaskify
pip install -r requirements.txt
```

## Running

```bash
python .\pytaskify\cli.py --version
```

## Coding

We follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) to maintain a good quality of code written, please read carefully to write correctly to keep the code organized and clean.

## Linter

We use [PyLint](https://pypi.org/project/Pylint/) to keep the code organized. Make sure your IDE is respecting the `.editorconfig` file, you may need to install a [plugin or extension](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).

To check for programming errors, bugs, stylistic errors and suspicious constructions you can run the command:

```bash
python .\pytaskify\cli.py lint
```

## Unit Test

```bash
python .\pytaskify\cli.py test
```

## IDE

Feel free to use any IDE, but we do recommend [VS Code](https://code.visualstudio.com/).

## Pull Request

If you want to contribute to `pyTaskify`, follow these steps:

1. Fork this repository
2. Create a new branch (`git checkout -b my-new-feature`)
3. Make your changes and commit (`git commit -am 'I added a new feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Open a Pull Request

# TODO

- Unit Tests
- Github workflow
- Github issue template
- Do not allow tasks with required arguments to be added as a dependency of another task, or allow passing the necessary arguments
- Dotenv file support
- Parallel execution of tasks
- Task timeout
- Dynamic variables
- Forwarding CLI arguments to commands
- Task status to prevent unnecessary work
- Platform specific tasks and commands
- Dry run mode
- Watch tasks

# Changelog

See [CHANGELOG](CHANGELOG.md) for a list of changes.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Acknowledgment

This project was inspired by [Task](https://taskfile.dev/) written in Go.

# Citation

If you rely on pytask to manage your research project, please cite it with the following
key to help others to discover the tool.

```bibtex
@Unpublished{Vilela2023,
    Title  = {A Task Runner written in Python.},
    Author = {Alison Vilela},
    Year   = {2023},
    Url    = {https://github.com/AlisonVilela/pyTaskify}
}
```
