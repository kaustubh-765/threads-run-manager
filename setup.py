from setuptools import setup, find_packages

setup(
    name="taskrunner",
    version="1.0.0",
    packages=find_packages(),
    # install_requires=["click"],   # or argparse, typer, etc.
    install_requires=["argparse"],   # or argparse, typer, etc.
    entry_points={
        "console_scripts": [
            "taskrunner=taskrunner.cli:main",   # <- CLI hook
        ],
    },
    description="A persistent CLI task runner with PID tracking",
    author="Kaustubh",
    python_requires=">=3.6",
)
