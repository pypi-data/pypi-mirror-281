import sys
import argparse

from simple_build_tools import configure_python_for_nexus
from simple_build_tools import configure_flake
from simple_build_tools import configure_gitignore

CHOICES = {
    "nexus": ("Setup project to use Nexus is PyPi source", configure_python_for_nexus),
    "flake8": ("Add a .flake8 config file to the project folder", configure_flake),
    "gitignore": ("Add a stndard gitignore to thep roject folder", configure_gitignore)
}


def get_help():
    rv = ""
    for choice, (help, _) in CHOICES.items():
        rv += f"{choice}: {help}\n"
    return rv


def run(args):
    parser = argparse.ArgumentParser(
        description="Tools to setup environment for Python Nexus",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("command", help=get_help(), choices=CHOICES.keys())

    v = vars(parser.parse_args(args))
    command = v["command"]
    if command in CHOICES:
        CHOICES[command][1]()


def main():
    run(sys.argv[1:])
