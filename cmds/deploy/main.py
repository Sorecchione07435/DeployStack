import argparse
import sys

from ...utils.core import colors

from .generator import generate_config_file, config_openstack
from .runner import deploy as runner_deploy

def init_parser(subparsers):
     
    parser = subparsers.add_parser(
    "deploy",
    help="Start the OpenStack Deployment on the current node"
)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--allinone",
        action="store_true",
        help="Runs a complete OpenStack deployment using an automatically generated configuration."
    )

    group.add_argument(
        "--config-file",
        help="Path to the configuration file"
    )

    parser.add_argument(
        "--install-cinder",
        type=str,
        choices=["yes", "no"],
        default="yes",
        help="Choosing whether to install Cinder (Block Storage) service (yes/no)"
    )

    parser.add_argument(
        "--install-horizon",
        type=str,
        choices=["yes", "no"],
        default="yes",
        help="Choosing whether to install Horizon (Dashboard) service (yes/no)"
    )

    parser.add_argument(
        "--lvm-image-size-in-gb",
        type=int,
        default=5,
        help="Size of the Cinder LVM image in GB (default: 5)"
    )

    parser.add_argument(
        "--neutron-driver",
        type=str,
        choices=["ovs", "ovn"],
        default="ovs",
        dest="neutron_driver",
        help="The Neutron Driver that will be used to configure networks in OpenStack"
    )

    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Generates a pre-compiled configuration file for the current system without starting the deployment"
    )

    return parser

def deploy(parser, args) -> None:

    if args.allinone:
        config_file_path = generate_config_file()
        
        cinder_flag = args.install_cinder
        horizon_flag = args.install_horizon
        driver = args.neutron_driver if args.neutron_driver in ("ovs","ovn") else "ovs"
        
        lvm_size = args.lvm_image_size_in_gb if cinder_flag == "yes" else 0
        
        config_openstack(
            install_horizon=horizon_flag,
            install_cinder=cinder_flag,
            config_file_path=config_file_path,
            lvm_image_size_in_gb=lvm_size,
            neutron_driver=driver
        )

        if args.generate_only:
            print(f"{colors.GREEN}Configuration file generated in '{config_file_path}{colors.RESET}'\n")
            print(f"You can start the deployment later with 'deploystack deploy --config-file {config_file_path}'")
            sys.exit(0)

        runner_deploy(config_file_path) 
    else:

        if args.config_file is None or not os.path.exists(args.config_file):
            print(f"{colors.RED}Configuration file not found. Generate it first using 'deploystack generate-config <file>'{colors.RESET}")
            sys.exit(1)
            
        runner_deploy(args.config_file) 
