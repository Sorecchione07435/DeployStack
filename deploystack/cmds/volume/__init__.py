from .create import init_parser as create_init_parser
from .attach import init_parser as attach_init_parser
from .detach import init_parser as detach_init_parser

def init_parser(subparsers):

    volume_parser = subparsers.add_parser(
        name="volume",
        help="Manage volumes"
    )

    volume_subparsers =  volume_parser.add_subparsers(
        dest="volume_cmd",
        metavar="<command>",
        required=True
    )

    create_init_parser(volume_subparsers)
    attach_init_parser(volume_subparsers)
    detach_init_parser(volume_subparsers)

def volume(parser, args) -> None:

    if args.volume_cmd == "create":
        from .create.main import create
        create(parser, args)
    elif args.volume_cmd == "attach":
        from .attach.main import attach
        attach(parser, args)
    elif args.volume_cmd == "detach":
        from .detach.main import detach
        detach(parser, args)
