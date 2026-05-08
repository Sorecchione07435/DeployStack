import argparse
import os as os_module
import sys

from ....utils.tasks.check_deployment import is_openstack_ready
from .runner import remove_image

def init_parser(subparsers):

    parser = subparsers.add_parser(
        "remove",
        help="Delete an existing image in the cloud"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--image-id",
        dest="image_id",
        help="Glance Image ID"
    )

    group.add_argument(
        "--image-name",
        dest="image_name",
        help="Glance Image Name"
    )

    parser.add_argument(
        "--timeout",
        default=300,
        dest="timeout",
        type=int,
        help="Maximum time to wait to check if the image has been deleted in OpenStack (default: 300s)"
    )

def remove(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit(1)

    if not is_openstack_ready():
        sys.exit(1)

    if args.image_id:
        remove_image(None, args.image_id, args.timeout)
    elif args.image_name:
        remove_image(args.image_name, None, args.timeout)

   