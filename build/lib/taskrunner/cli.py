import argparse
from . import manager
import click

@click.group()
def main():
    parser = argparse.ArgumentParser(description="Persistent Task Runner CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("cmd", help="Command to run", nargs="+")
    
    parser_remove = subparsers.add_parser("remove", help="Remove a task")
    parser_remove.add_argument("index", type=int, help="Task index to remove")
    
    subparsers.add_parser("list", help="List tasks")
    subparsers.add_parser("run", help="Run task monitor")
    
    args = parser.parse_args()
    
    if args.command == "add":
        manager.add_task(" ".join(args.cmd))
    elif args.command == "remove":
        manager.remove_task(args.index)
    elif args.command == "list":
        manager.list_tasks()
    elif args.command == "run":
        manager.run_monitor()
    else: 
        parser.print_help()

@main.command()
def list():
    click.echo("Listing tasks...")

@main.command()
@click.argument("cmd")
def add(cmd):
    click.echo(f"Adding task: {cmd}")