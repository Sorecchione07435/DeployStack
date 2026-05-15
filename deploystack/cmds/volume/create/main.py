import sys

from .runner import create as create_volume

from ....utils.tasks.check_deployment import is_openstack_ready, is_cinder_installed

def init_parser(subparsers):

    parser = subparsers.add_parser(
        "create",
        help="Create a new volume"
    )

    parser.add_argument(
        "--name",
        required=True,
        help="The name of the volume to create (required)"
    )

    parser.add_argument(
        "--size",
        default=5,
        help="The size of the volume in GB (default: 5 GB)"
    )

    parser.add_argument(
        "--is-bootable",
        action="store_true",
        help="Mark the volume as bootable. Use this flag if the volume should be usable as a boot disk."
    )

    parser.add_argument(
        "--image",
        help="Optional Glance image ID or name to create the volume from."
    )

def create(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit(1)

    if not is_openstack_ready():
        sys.exit(1)

    if not is_cinder_installed():
        sys.exit(1)

    create_volume(
        args.name,
        args.size,
        args.is_bootable,
        args.image
    )


        