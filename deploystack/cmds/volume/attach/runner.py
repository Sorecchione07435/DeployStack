import subprocess
import sys

from ....utils.core import colors

from ...shell import logger

def attach_volume(volume: str, instance: str):

    attach_volume_cmd = [
            "openstack", "server", "add",
            "volume", instance, volume
        ]

    try:
        subprocess.run(attach_volume_cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"{colors.RED}Error while trying to attach volume: {e}\n{e.stderr}{colors.RESET}")
        sys.exit(1)

def attach(
    volume: str,
    instance: str
):
    
    print(f"Attaching the volume '{volume}' to instance '{instance}' ...\n")

    attach_volume(volume, instance)

    print(f"Volume '{volume}' successfully attached to '{instance}' Instance")

