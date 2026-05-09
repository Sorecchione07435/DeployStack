import subprocess

from ..utils.core.commands import run_command
from ..utils.apt.apt import apt_install, apt_update
from ..utils.config.parser import get
from ..utils.core.system_utils import nc_wait
from ..utils.core import colors

def set_openstack_release(config):
    release = get(config, "openstack.OPENSTACK_RELEASE", "caracal").lower()

    distro = subprocess.check_output(["lsb_release", "-cs"]).decode().strip()
    repo_line = f"deb http://ubuntu-cloud.archive.canonical.com/ubuntu {distro}-{release} main"
    repo_file = f"/etc/apt/sources.list.d/cloud-archive-{release}.list"

    with open(repo_file, "w") as f:
        f.write(repo_line + "\n")

    run_command(["apt-get", "update" "-y"], f"Updating package lists for {release}", ignore_errors=True)

def install_pkgs():

    print()
    
    if not apt_update() : return False

    if not apt_install(["wget", "rabbitmq-server", "python3-openstackclient", "memcached"], ux_text=f"Installing prerequisite packages..."): return False

    return True


def add_rabbitmq_openstack_user(config):
     
    print()

    rabbitmq_password = get(config, "passwords.RABBITMQ_PASSWORD")

    try:
        output = subprocess.check_output(["rabbitmqctl", "list_users"], text=True)
        user_exists = "openstack" in output
    except subprocess.CalledProcessError:
        user_exists = False

    if not user_exists:
        if not run_command(
            ["rabbitmqctl", "add_user", "openstack", rabbitmq_password],
            "Creating RabbitMQ OpenStack User..."
        ): return False

    if not run_command(
        ["rabbitmqctl", "set_permissions", "openstack", ".*", ".*", ".*"],
        "Setting permissions for RabbitMQ OpenStack User..."
    ): return False
    
    return True

def run_setup_prereqs(config):

    ip_address = get(config, "network.HOST_IP")

    set_openstack_release(config)
    if not install_pkgs(): return False

    if not nc_wait(ip_address, 5672) : return False
    if not add_rabbitmq_openstack_user(config): return False

    print(f"\n{colors.GREEN}Prerequisites configured successfully!{colors.RESET}\n")
    return True