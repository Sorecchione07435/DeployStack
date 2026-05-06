import argparse
import ipaddress
import os
import shutil
import sys
import uuid

from .cli import build_parser, colors, COMMANDS

def print_banner():
    print(f"{colors.BRIGHT_BLUE}Welcome to DeployStack Utility{colors.RESET}\n")

def main():
    print_banner()

    if os.geteuid() != 0:
        print(f"{colors.RED}This utility must be run as root.{colors.RESET}")
        print(f"{colors.YELLOW}Try: sudo <command>{colors.RESET}\n")
        sys.exit(1)

    parser = build_parser()
    # Only parse known args to avoid automatic error exit
    args, unknown = parser.parse_known_args()

    if args.command is None:
        print(f"{colors.YELLOW}No command provided. Available commands:{colors.RESET}\n")
        parser.print_help()
        print(f"\nTip: Run '{colors.BRIGHT_BLUE}deploystack <command> --help{colors.RESET}' for detailed usage of each command.")
        sys.exit(1)

    COMMANDS[args.command](parser, args)