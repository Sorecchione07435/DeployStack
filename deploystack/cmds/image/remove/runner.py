import subprocess
import time
import sys

from ...shell import _run
from ....utils.core import colors

def remove_glance_image(identifier: str, timeout: int = 30) -> bool:
    remove_image_cmd = ["openstack", "image", "delete", identifier]

    try:
        _run(remove_image_cmd, True)
    except subprocess.CalledProcessError as e:
        print(f"{colors.RED}Error while trying to delete image: {e}{colors.RESET}")
        return False

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                ["openstack", "image", "list", "-f", "value", "-c", "ID"],
                capture_output=True,
                text=True,
                check=True
            )
            image_ids = result.stdout.splitlines()
            if identifier not in image_ids:
                return True
        except subprocess.CalledProcessError:
            pass
        time.sleep(2)

    print(f"{colors.RED}Timeout: image {identifier} was not deleted.{colors.RESET}")
    return False

def remove_image(
        image_name: str,
        image_id: str,
        timeout: int
):
    
    image_identifier: str
    
    if image_id:
        image_identifier = image_id
        print(f"Removing image with ID: {image_id} ...")
    elif image_name:
        image_identifier = image_name
        print(f"Removing image with Name: {image_name} ...")

    if remove_glance_image(image_identifier, timeout):
        print(f"\n{colors.GREEN}Image '{image_identifier}' successfully deleted{colors.RESET}")
    else:
        sys.exit(1)

    

    
