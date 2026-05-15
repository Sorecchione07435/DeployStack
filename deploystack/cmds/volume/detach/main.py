import sys

from ....utils.tasks.check_deployment import is_openstack_ready, is_cinder_installed

def init_parser(subparsers):

    parser = subparsers.add_parser(
        "detach",
        help="Detach a volume that is currently attached to an instance"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--volume-id",
        dest="volume_id",
        help="ID of the volume to detach. Either --volume-id or --volume-name must be provided."
    )
    group.add_argument(
        "--volume-name",
        dest="volume_name",
        help="Name of the volume to detach. Either --volume-id or --volume-name must be provided."
    )

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument(
        "--instance-id",
        dest="instance_id",
        help="ID of the instance from which to detach the volume. Either --instance-id or --instance-name must be provided."
    )
    group2.add_argument(
        "--instance-name",
        dest="instance_name",
        help="Name of the instance from which to detach the volume. Either --instance-id or --instance-name must be provided."
    )

def detach(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit(1)

    if not is_openstack_ready():
        sys.exit(1)

    if not is_cinder_installed():
        sys.exit(1)

