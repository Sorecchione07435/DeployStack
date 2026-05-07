import argparse
import os as os_module

from ....utils.core import colors

from ....utils.tasks.check_deployment import check_deployment, check_env_variables, MARKER_FILE

from .runner import upload_image

def init_parser(subparsers):

    parser = subparsers.add_parser(
        "upload",
        help="Upload a new, ready-made cloud image into Glance from the web"
    )

    parser.add_argument(
        "--name",
        dest="image_name",
        help="Custom image name (if not provided, a default name will be used)"
    )

    parser.add_argument(
        "--arch",
        choices=["amd64", "arm64", "x86_64", "aarch64"],
        default="amd64",
        help="CPU architecture of the image (default: amd64)"
    )

    parser.add_argument(
        "--os",
        required=True,
        help="OS name of the cloud image to upload"
    )

    parser.add_argument(
        "--version",
        required=True,
        help="OS version of the cloud image to upload"
    )

    parser.add_argument(
        "--visibility",
        choices=["public", "private", "shared"],
        help="Visibility of the image in Glance (default: public)"
    )

    parser.add_argument(
        "--output-dir",
        default="/tmp",
        dest="output_dir",
        help="Directory where the image will be downloaded before upload (default: /tmp)"
    )

    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep the downloaded image file after upload instead of deleting it"
    )

    parser.add_argument(
        "--timeout",
        default=15,
        dest="timeout",
        type=int,
        help="Maximum time in seconds to wait for the uploaded image to reach the ACTIVE state in OpenStack"
    )

def upload(parser, args) -> None:

    if args.command is None:
        parser.print_help()
        parser.exit(1)

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

    upload_image(
        args.os,
        args.version,
        args.visibility,
        args.output_dir,
        args.keep,
        args.arch,
        args.timeout
    )
