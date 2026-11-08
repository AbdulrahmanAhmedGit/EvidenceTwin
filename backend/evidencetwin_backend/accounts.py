"""Operator account commands that can run beside the active single-process service.

No Flask application, worker, provider dispatch or public registration is created.
"""
import click
from .config import load_config
from .services.access import register_account_commands
from .services.store import Store


def main():
    commands = click.Group(help='Provision and revoke EvidenceTwin pilot accounts. Passwords are prompted privately.')
    register_account_commands(commands, Store(load_config()['DATA_DIRECTORY']))
    commands()


if __name__ == '__main__':
    main()
