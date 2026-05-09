import subprocess
import time
import sys
import re

from ...shell import _run
from ....utils.core import colors


def is_uuid(identifier) -> bool:
    uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.fullmatch(uuid_regex, identifier.lower()))

def get_image_name_from_uuid(uuid) -> str:

    get_image_name_cmd = [
        "openstack", "image", "show", uuid, "-f", "value", "-c", "name"
    ]

    try:
        result = subprocess.run(get_image_name_cmd, capture_output=True, text=True, check=True)

        image_name = result.stdout.strip()

        if image_name is not "":
            return image_name
        else:
            image_name = ""
            
    except subprocess.CalledProcessError as e:
        print(f"\n{colors.RED}Error while trying to getting image name: {e}{colors.RESET}")
        sys.exit(1)


def check_image_running_instances(identifier: str) -> bool:

    image_name: str

    check_images_instances_cmd = [
        "openstack", "server", "list", "-f", "value", "-c", "Image"
    ]

    if is_uuid(identifier):
        image_name = get_image_name_from_uuid(identifier)
    else:
        image_name = identifier

    try:
        result = subprocess.run(check_images_instances_cmd, capture_output=True, text=True, check=True)
        running_image_names = [line.strip() for line in result.stdout.splitlines()]

        return image_name in running_image_names
        
    except subprocess.CalledProcessError as e:
        print(f"\n{colors.RED}Error while trying to listing images: {e}{colors.RESET}")
        sys.exit(1)


def remove_glance_image(identifier: str, timeout: int = 30) -> bool:
    remove_image_cmd = ["openstack", "image", "delete", identifier]

    try:
        _run(remove_image_cmd, True)
    except subprocess.CalledProcessError as e:
        print(f"\n{colors.RED}Error while trying to delete image: {e}{colors.RESET}")
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

    print(f"\n{colors.RED}Timeout: image {identifier} was not deleted.{colors.RESET}")
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

    if check_image_running_instances(image_identifier):
        print(f"{colors.RED}Error: There are instances still running with the '{image_identifier}' image. Please stop them before attempting removal.{colors.RESET}")
        sys.exit(1)

    if remove_glance_image(image_identifier, timeout):
        print(f"\n{colors.GREEN}Image '{image_identifier}' successfully deleted{colors.RESET}")
    else:
        sys.exit(1)

    

    
