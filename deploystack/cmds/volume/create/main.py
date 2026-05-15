import sys

from ....utils.tasks.check_deployment import is_openstack_ready, is_cinder_installed

def init_parser(subparsers):

    parser = subparsers.add_parser(
        "create",
        help="Create a new volume"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    
    parser.add_argument(
        "--volume-name",
        required=True,
        help="The name of the volume to create (required)"
    )

    parser.add_argument(
        "--volume-size",
        default=5,
        help="The size of the volume in GB (default: 5 GB)"
    )

    parser.add_argument(
        "--is-bootable",
        action="store_true",
        help="Mark the volume as bootable. Use this flag if the volume should be usable as a boot disk."
    )

    group.add_argument(
        "--image-id",
        dest="image_id",
        help="Glance Image ID. One of --image-id or --image-name must be provided."
    )

    group.add_argument(
        "--image-name",
        dest="image_name",
        help="Glance Image Name. One of --image-id or --image-name must be provided."
    )

def create(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit(1)

    if not is_openstack_ready():
        sys.exit(1)

    if not is_cinder_installed():
        sys.exit(1)

        