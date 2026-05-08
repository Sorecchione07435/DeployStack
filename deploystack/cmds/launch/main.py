import uuid
import sys

from ...utils.tasks.check_deployment import is_openstack_ready
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

    if not is_openstack_ready():
        sys.exit(1)

    launch_instance(name=args.name, image=args.image, flavor=args.flavor, network=args.network, keypair=args.keypair, password=args.password)
