import argparse
import uuid
import os

from ...utils.core import colors

from ...utils.tasks.check_deployment import check_deployment, check_env_variables, MARKER_FILE 
from .runner import launch as launch_instance

def init_parser(subparsers): 

    parser = subparsers.add_parser(
    "launch",
    help="Launch an OpenStack instance"
)

    parser.add_argument(
        "--name",
        default=f"instance-{uuid.uuid4().hex[:8]}",
        help="Name of the instance to launch. Defaults to a random generic instance name."
        )
    
    parser.add_argument(
        "--image",
        default="cirros",
        help="Name of the image to use for the instance. Defaults to 'cirros'."
    )

    parser.add_argument(
        "--flavor",
        default="m1.tiny",
        help="Flavor (size) of the instance. Defaults to 'm1.tiny'."
    )

    parser.add_argument(
        "--network",
        default="internal",
        help="Network to attach the instance to. Defaults to 'internal'."
    )

    parser.add_argument(
        "--keypair",
        default="",
        help="Existing key pair in OpenStack to associate with the instance"
    )

    parser.add_argument(
        "--password",
        default="",
        help="Password for the admin instance user."
    )

    return parser

def launch(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit()

    base_check = check_deployment(include_endpoints=False)
    if not base_check.ok or not os.path.exists(MARKER_FILE):
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

    launch_instance(name=args.name, image=args.image, flavor=args.flavor, network=args.network, keypair=args.keypair, password=args.password)
