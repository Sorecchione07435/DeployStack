import subprocess
import os

from ..utils.core.commands import run_command
from ..utils.apt.apt import apt_install, apt_update
from ..utils.config.parser import get
from ..utils.core.system_utils import nc_wait
from ..utils.core import colors

UBUNTU_CLOUD_ARCHIVE = {
    ("focal",   "yoga"):      "focal-updates/yoga",
    ("focal",   "zed"):       "focal-updates/zed",
    ("jammy",   "yoga"):      "jammy-updates/yoga",
    ("jammy",   "zed"):       "jammy-updates/zed",
    ("jammy",   "antelope"):  "jammy-updates/antelope",
    ("jammy",   "bobcat"):    "jammy-updates/bobcat",
    ("jammy",   "caracal"):   "jammy-updates/caracal",
    ("noble",   "dalmatian"): "noble-updates/dalmatian",
    ("noble",   "epoxy"):     "noble-updates/epoxy",
}

UBUNTU_NATIVE_OPENSTACK = {
    "focal":    "ussuri",
    "jammy":    "yoga",
    "noble":    "caracal",
    "resolute": "gazpacho",
}

def _add_uca_repo(pocket: str, release: str):
    keyring_path = "/etc/apt/keyrings/ubuntu-cloud-archive.gpg"
    repo_file = f"/etc/apt/sources.list.d/cloud-archive-{release}.list"

    if not os.path.exists(keyring_path):
        run_command(
            [
                "bash", "-c",
                f"gpg --keyserver keyserver.ubuntu.com --recv-keys EC4926EA "
                f"&& gpg --export EC4926EA > {keyring_path}"
            ],
            "Adding Ubuntu Cloud Archive GPG key...",
            ignore_errors=False
        )

    repo_line = (
        f"deb [signed-by={keyring_path}] "
        f"http://ubuntu-cloud.archive.canonical.com/ubuntu {pocket} main"
    )
    with open(repo_file, "w") as f:
        f.write(repo_line + "\n")

    print(f"{colors.GREEN}Added UCA repo: {pocket}{colors.RESET}")


def _setup_debian_repo(distro_codename: str, release: str):
    dpkg_conf = "/etc/apt/apt.conf.d/90force-conf"
    repo_file = "/etc/apt/sources.list.d/debian-backports.list"
    repo_line = f"deb http://deb.debian.org/debian {distro_codename}-backports main"

    if not os.path.exists(repo_file):
        with open(repo_file, "w") as f:
            f.write(repo_line + "\n")

    subprocess.run(
        'echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections',
        shell=True, check=True
    )
    with open(dpkg_conf, "w") as f:
        f.write('DPkg::Options {"--force-confdef"; "--force-confold"; };')

    print(f"{colors.YELLOW}Debian: OpenStack packages from backports. "
          f"Version '{release}' may not be guaranteed.{colors.RESET}")


def set_openstack_release(config):
    release = get(config, "openstack.OPENSTACK_RELEASE", "caracal").lower()

    try:
        distro_id = subprocess.check_output(
            ["lsb_release", "-is"], stderr=subprocess.DEVNULL
        ).decode().strip().lower()
        distro_codename = subprocess.check_output(
            ["lsb_release", "-cs"], stderr=subprocess.DEVNULL
        ).decode().strip().lower()
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to detect Linux distribution{colors.RESET}")
        return False

    if distro_id == "ubuntu":
        native = UBUNTU_NATIVE_OPENSTACK.get(distro_codename)

        if native == release:
            print(f"{colors.GREEN}OpenStack {release} is natively available "
                  f"on Ubuntu {distro_codename}, skipping Cloud Archive.{colors.RESET}")

        elif (distro_codename, release) in UBUNTU_CLOUD_ARCHIVE:
            pocket = UBUNTU_CLOUD_ARCHIVE[(distro_codename, release)]
            _add_uca_repo(pocket, release)

        else:
            print(f"{colors.RED}OpenStack '{release}' is not supported "
                  f"on Ubuntu '{distro_codename}'.{colors.RESET}")
            print(f"{colors.YELLOW}Supported combinations:{colors.RESET}")
            for (codename, rel), pocket in UBUNTU_CLOUD_ARCHIVE.items():
                print(f"  Ubuntu {codename} -> {rel} ({pocket})")
            if native:
                print(f"  Ubuntu {distro_codename} -> {native} (native, no UCA needed)")
            return False

    elif distro_id == "debian":
        _setup_debian_repo(distro_codename, release)

    else:
        print(f"{colors.YELLOW}Warning: Unknown distribution '{distro_id}'. "
              f"Skipping repository setup.{colors.RESET}")

    if not apt_update():
        return False

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