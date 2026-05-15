import subprocess
import sys

from ....utils.core import colors

from ...shell import _run, _os, _os_value, logger

def mark_as_bootable(id: str):

    set_bootable_cmd = [
        "openstack", "volume", "set",
        "--bootable", id
    ]

    try:
        subprocess.run(set_bootable_cmd, capture_output=True, text=True, check=True)
        logger.info(f"{colors.GREEN}Volume {id} marked as bootable successfully.{colors.RESET}\n")

    except subprocess.CalledProcessError as e:
            logger.error(f"{colors.RED}Error while trying to setting bootable attribute on volume: {e}{colors.RESET}")
            sys.exit(1)
    

def create_volume(name: str, size: int, image: str = None) -> str:
    """
    Create a volume with or without an image. Returns the volume ID as string.
    """
    size_str = str(size)

    if image:
        cmd = [
            "openstack", "volume", "create",
            "--size", size_str,
            "--image", image,
            name,
            "-f", "value", "-c", "id"
        ]
    else:
        cmd = [
            "openstack", "volume", "create",
            "--size", size_str,
            name,
            "-f", "value", "-c", "id"
        ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        volume_id = result.stdout.strip()
        return volume_id
    except subprocess.CalledProcessError as e:
        logger.error(f"{colors.RED}Error while trying to create volume: {e}\n{e.stderr}{colors.RESET}")
        sys.exit(1)


def create(
    volume_name: str,
    volume_size: int,
    is_bootable: bool,
    image: str = None
) -> None:

    mark_bootable_flag = is_bootable and not image

    if is_bootable and image:
        logger.warning(
            f"{colors.YELLOW}The --is-bootable flag is redundant when creating a volume from an image; "
            f"the volume will automatically be bootable.{colors.RESET}\n"
        )

    print(f"Creating the volume '{volume_name}' ...\n")
    volume_id = create_volume(volume_name, volume_size, image)

    if mark_bootable_flag:
        print("Marking volume as bootable ...\n")
        mark_as_bootable(volume_id)

    print(f"{colors.GREEN}Volume '{volume_name}' (ID: {volume_id}) successfully created!{colors.RESET}")