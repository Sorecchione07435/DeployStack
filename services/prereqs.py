from ..utils.run_command_utils import run_command
from ..utils.apt_utils import apt_install, apt_update
from ..utils.config_parser import parse_config, get
from ..utils import colors

import subprocess

def set_openstack_release(config):
    release = get(config, "OPENSTACK_RELEASE", "caracal")
    message = f"Adding repository for {release} OpenStack Release..."
    cmd = ["add-apt-repository", f"cloud-archive:{release}", "-y"]

    _ = run_command(cmd, message, ignore_errors=True)

    #print(f"Repository setup for OpenStack release '{release}' attempted. Any errors are non-critical.\n")

def install_pkgs():
    apt_update()

    packages = ["wget", "rabbitmq-server", "python3-openstackclient", "memcached"]

    success =  apt_install(packages, ux_text=f"Installing prerequisite packages...")

    if not success:
            #print(f"Installation of packages failed. Aborting installation.")
            return False
    return True

def add_rabbitmq_openstack_user(config):
     
    print()

    rabbitmq_password = get(config, "RABBITMQ_PASSWORD")

    try:
        output = subprocess.check_output(["rabbitmqctl", "list_users"], text=True)
        user_exists = "openstack" in output
    except subprocess.CalledProcessError:
        user_exists = False

    if not user_exists:
        if not run_command(
            ["rabbitmqctl", "add_user", "openstack", rabbitmq_password],
            "Creating RabbitMQ OpenStack User..."
        ):
            return False

    if not run_command(
        ["rabbitmqctl", "set_permissions", "openstack", ".*", ".*", ".*"],
        "Setting permissions for RabbitMQ OpenStack User..."
    ):
        return False
    
    return True

def run_setup_prereqs(config):

    set_openstack_release(config)

    if not install_pkgs():
        #print(f"\n{colors.RED}Prerequisite installation failed. Aborting.{colors.RESET}")
        return False
    
    if not add_rabbitmq_openstack_user(config):
        return False

    print(f"\n{colors.GREEN}Prerequisites configured successfully!{colors.RESET}\n")
    return True