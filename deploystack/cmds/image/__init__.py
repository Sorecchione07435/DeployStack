import argparse

from .upload.main import init_parser as upload_init_parser
from .remove.main import init_parser as remove_init_parser

def init_parser(subparsers):

    image_parser = subparsers.add_parser(
        name="image",
        help="Manage cloud images"
    )

    image_subparsers = image_parser.add_subparsers(
        dest="image_cmd",
        metavar="<command>",
        required=True
    )

    upload_init_parser(image_subparsers)
    remove_init_parser(image_subparsers)

def image(parser, args) -> None:

    if args.image_cmd == "upload":
        from .upload.main import upload
        upload(parser, args)
    elif args.image_cmd == "remove":
        from .remove.main import remove
        remove(parser, args)