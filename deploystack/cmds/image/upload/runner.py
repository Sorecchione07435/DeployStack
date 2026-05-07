import requests
import os as os_module
import tempfile
import itertools
import subprocess
import time
import sys

from tqdm import tqdm

from ....utils.core import colors

from ...shell import _run, _os, _os_value

from .dictionary import get_image_url, get_latest_centos_url

def generate_temp_filename(os_name: str, version: str, arch: str, ext: str = ".qcow2", temp_dir: str = None) -> str:

    if temp_dir is None:
        temp_dir = tempfile.gettempdir()
    filename = f"{os_name}-{version}-{arch}{ext}"
    return os_module.path.join(temp_dir, filename)

def download_file(url: str, output_path: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    chunk_size = 1024 * 1024  # 1 MB
    downloaded = 0

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = int(downloaded / total_size * 100)

                sys.stdout.write(
                    f"\rDownloading {os_module.path.basename(output_path)}: {percent}% "
                )
                sys.stdout.flush()

    sys.stdout.write(
        f"\rDownloading {os_module.path.basename(output_path)}: 100%\n"
    )
    sys.stdout.flush()

def wait_for_image(image_name, timeout=300):
    start = time.time()
    while True:
        result = subprocess.run(
            ["openstack", "image", "show", image_name, "-f", "value", "-c", "status"],
            capture_output=True, text=True
        )
        status = result.stdout.strip()
        print(f"\rWaiting for image '{image_name}' to become active: {status}", end="")
        if status.lower() == "active":
            break
        if time.time() - start > timeout:
            raise TimeoutError(f"Image {image_name} did not become active in {timeout} seconds")
        time.sleep(5)
    print()  # vai a capo alla fine

def upload_glance_image(
        filepath: str,
        name: str,
        os: str,
        visibility: str,
        timeout: int
    ):
    
    print(f"\nUploading image '{name}' ...\n")

    create_image_cmd = [
        "openstack", "image", "create",
        "--container-format", "bare",
        "--disk-format", "qcow2",
        "--file", filepath,
        "--property", "os_type=linux",
        "--property", f"os_distro={os}",
        "--property", "os_admin_user=root"
    ]

    if visibility == "public":
        create_image_cmd.append("--public")
    elif visibility == "private":
        create_image_cmd.append("--private")
    elif visibility == "shared":
        create_image_cmd.append("--shared")

    create_image_cmd.append(f"{name}")
    
    try:
        result = _run(create_image_cmd)

        wait_for_image(name, timeout)

        return True
    except subprocess.CalledProcessError as e:
        print(f"{colors.RED}Failed to create image: {e}{colors.RESET}")
        sys.exit(1)
    except TimeoutError as e:
        print(f"{colors.RED}{e}{colors.RESET}")
        sys.exit(1)

def upload_image(
    os: str,
    version: str,
    visibility: str,
    output_dir: str,
    keep: bool,
    arch: str,
    timeout: int
):
    
    print("Getting the Download URL for the image...\n")
    image_url = get_image_url(os, version, arch)

    if not output_dir:
        output_dir = "/tmp"

    temp_file_path = generate_temp_filename(os, version, arch, temp_dir=output_dir)
    temp_file_name = os_module.path.splitext(os_module.path.basename(temp_file_path))[0]

    download_file(image_url, temp_file_path)

    if upload_glance_image(temp_file_path, temp_file_name, os, visibility, timeout):
        print(f"\n{colors.GREEN}Image successfully uploaded{colors.RESET}")
        print()
        print(f"You can now launch instances with the new image uploaded with 'deploystack launch --image {temp_file_name}'")

    if not keep:
        os_module.remove(temp_file_path)