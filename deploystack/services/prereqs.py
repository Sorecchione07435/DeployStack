import subprocess
import os

from ..utils.core.commands import run_command
from ..utils.apt.apt import apt_install, apt_update
from ..utils.config.parser import get
from ..utils.core.system_utils import nc_wait
from ..utils.core import colors

def set_openstack_release(config):

  
    UBUNTU_CLOUD_ARCHIVE_CODENAMES = {
    "jammy":  "jammy-updates/caracal",   # Ubuntu 22.04
    "focal":  "focal-updates/yoga",       # Ubuntu 20.04
}
    
    release = get(config, "openstack.OPENSTACK_RELEASE", "caracal").lower()

    try:
        distro_id = subprocess.check_output(["lsb_release", "-is"]).decode().strip().lower()
        distro_codename = subprocess.check_output(["lsb_release", "-cs"]).decode().strip().lower()
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to detect Linux distribution{colors.RESET}")
        return False

    if distro_id == "ubuntu":
        if distro_codename in UBUNTU_CLOUD_ARCHIVE_CODENAMES:
            pocket = UBUNTU_CLOUD_ARCHIVE_CODENAMES[distro_codename]
            repo_line = f"deb http://ubuntu-cloud.archive.canonical.com/ubuntu {pocket} main"
            repo_file = f"/etc/apt/sources.list.d/cloud-archive-{release}.list"

            run_command(
                ["apt-key", "adv", "--keyserver", "keyserver.ubuntu.com", "--recv-keys", "EC4926EA"],
                "Adding Ubuntu Cloud Archive keyring...", ignore_errors=True
            )

            with open(repo_file, "w") as f:
                f.write(repo_line + "\n")
        else:
            print(f"{colors.YELLOW}Ubuntu {distro_codename}: OpenStack packages available in official repos, skipping Cloud Archive.{colors.RESET}\n")

    elif distro_id == "debian":

        dpkg_conf = '/etc/apt/apt.conf.d/90force-conf'
        repo_line = f"deb http://deb.debian.org/debian {distro_codename}-backports main"
        repo_file = f"/etc/apt/sources.list.d/debian-backports.list"

        if not os.path.exists(repo_file):
            with open(repo_file, "w") as f:
                f.write(repo_line + "\n")

        subprocess.run('echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections', shell=True, check=True)

        with open(dpkg_conf, 'w') as f:
            f.write('DPkg::Options {"--force-confdef"; "--force-confold"; };')
    else:
        print(f"{colors.YELLOW}Warning: Unknown distribution '{distro_id}'. Skipping repository setup.{colors.RESET}")

    if not apt_update(): return False

    return True

def install_pkgs():

    print()

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

    if not set_openstack_release(config): return False
    if not install_pkgs(): return False

    if not nc_wait(ip_address, 5672) : return False
    if not add_rabbitmq_openstack_user(config): return False

    print(f"\n{colors.GREEN}Prerequisites configured successfully!{colors.RESET}\n")
    return True