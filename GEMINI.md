# GEMINI.md

## Project Overview

This project is a Python-based CLI tool called **TaskRunner** for managing long-running background tasks. It allows users to add, list, and remove tasks, and it automatically monitors and restarts them if they fail.

The main technologies used are:
- **Python**: The core language for the application.
- **argparse**: For parsing command-line arguments and subcommands.
- **subprocess**: For running and managing background processes.
- **filelock**: For ensuring safe concurrent access to task and PID files.

The project is structured as a standard Python package with a `setup.py` file for installation and a `taskrunner` module containing the application logic. The core logic is split between `cli.py` for command-line handling and `manager.py` for task management.

Tasks are stored in a plain text file (`~/.taskrunner/tasks.txt`), and process IDs (PIDs) are tracked in a JSON file (`~/.taskrunner/pids.json`) to ensure clean process management.

## Building and Running

### Installation

To install the project in development mode, run the following command in the project root:

```bash
pip install -e .
```

This will install the `taskrunner` command-line tool.

### Running

The main commands are:

- **`taskrunner add "<command>"`**: Adds a new task to the task list.
- **`taskrunner remove <index>`**: Removes a task from the list by its index.
- **`taskrunner list`**: Lists all the current tasks.
- **`taskrunner run`**: Starts the task monitor, which runs in the foreground, managing the background tasks. The monitor can be stopped gracefully using `Ctrl+C`.

### Testing

There are no dedicated test files in the project. To test the functionality, you can manually run the commands and observe the behavior. For example:

1.  Add a task: `taskrunner add "ping -c 5 google.com"`
2.  List tasks: `taskrunner list`
3.  Run the monitor: `taskrunner run`
4.  In another terminal, check the running processes.
5.  Remove the task: `taskrunner remove 1`

## Development Conventions

- The project uses the standard Python library `argparse` for the CLI, not external libraries like `click` or `typer`.
- The code is organized into a `taskrunner` package.
- The `manager.py` module contains the core logic for task management, including starting, stopping, and monitoring processes.
- The `cli.py` module handles the command-line interface and calls the functions in `manager.py`.
- The project uses a simple logging mechanism that prints messages to the console with a timestamp.
- Tasks and PIDs are stored in a hidden directory in the user's home directory (`~/.taskrunner`).
- **Security Note**: The `subprocess.Popen` calls use `shell=True`. While convenient, this can pose a security risk if untrusted input is used as commands. For production environments or scenarios involving untrusted input, it is generally recommended to avoid `shell=True` and instead pass commands as a list of arguments.