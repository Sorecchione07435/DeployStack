import argparse

import os as os_module

from ....utils.core import colors

from ....utils.tasks.check_deployment import check_deployment, check_env_variables, MARKER_FILE 

def init_parser(subparsers):

    parser = subparsers.add_parser(
        "remove",
        help="Delete an existing image in the cloud"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--image-id",
        help="Glance Image ID"
    )

    group.add_argument(
        "--image-name",
        help="Glance Image Name"
    )


def remove(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit()

    base_check = check_deployment(include_endpoints=False)
    if not base_check.ok or not os_module.path.exists(MARKER_FILE):
        print(f"{colors.RED}OpenStack is not deployed yet.{colors.RESET}\n")
        print(f"{colors.YELLOW}  • Run 'deploy --allinone' for a full automated deployment{colors.RESET}")
        print(f"{colors.YELLOW}  • Or run 'deploy --config-file <config_file>' with a custom config{colors.RESET}\n")
        return

    try:
        check_env_variables()
    except RuntimeError:
        print(f"{colors.YELLOW}Shell is not authenticated. Source the environment file first:{colors.RESET}\n")
        print(f"  {colors.YELLOW}source /root/admin-openrc.sh{colors.RESET}  or")
        print(f"  {colors.GREEN}source /root/demo-openrc.sh{colors.RESET}\n")
        return

    endpoint_check = check_deployment(include_endpoints=True)
    if not endpoint_check.ok:
        print(f"{colors.RED}OpenStack is deployed but services are not fully operational:{colors.RESET}")
        print(endpoint_check)
        return