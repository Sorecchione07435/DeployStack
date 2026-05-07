
centos_version_map = {
    "10": "10-stream",
    "9":  "9-stream",
    "8":  "8-stream",
}

centos_version_urls = {
    "6": "https://cloud.centos.org/centos/6/images/",
    "7": "https://cloud.centos.org/centos/7/images/",
    "7+": "https://cloud.centos.org/centos/{internal_ver}/{arch}/images/"
}

debian_version_urls = {
    "11": "https://cdimage.debian.org/cdimage/cloud/bullseye/latest/debian-11-genericcloud-{arch}.qcow2",
    "12": "https://cdimage.debian.org/cdimage/cloud/bookworm/latest/debian-12-genericcloud-{arch}.qcow2",
    "13": "https://cdimage.debian.org/cdimage/cloud/trixie/latest/debian-13-genericcloud-{arch}.qcow2"
}

fedora_version_urls = {
    "22": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/22/Cloud/{arch}/Images/Fedora-Cloud-Base-22-20150521.{arch}.qcow2",
    "23": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/23/Cloud/{arch}/Images/Fedora-Cloud-Base-23-20151030.{arch}.qcow2",
    "24": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/24/CloudImages/{arch}/images/Fedora-Cloud-Base-24-1.2.{arch}.qcow2",
    "25": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/25/CloudImages/{arch}/images/Fedora-Cloud-Base-25-1.3.{arch}.qcow2",
    "26": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/26/CloudImages/{arch}/images/Fedora-Cloud-Base-26-1.5.{arch}.qcow2",
    "27": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/27/CloudImages/{arch}/images/Fedora-Cloud-Base-27-1.6.{arch}.qcow2",
    "28": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/28/Cloud/{arch}/images/Fedora-Cloud-Base-28-1.1.{arch}.qcow2",
    "29": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/29/Cloud/{arch}/images/Fedora-Cloud-Base-29-1.2.{arch}.qcow2",
    "30": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/30/Cloud/{arch}/images/Fedora-Cloud-Base-30-1.2.{arch}.qcow2",
    "31": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/31/Cloud/{arch}/images/Fedora-Cloud-Base-31-1.9.{arch}.qcow2",
    "32": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/32/Cloud/{arch}/images/Fedora-Cloud-Base-32-1.6.{arch}.qcow2",
    "33": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/33/Cloud/{arch}/images/Fedora-Cloud-Base-33-1.2.{arch}.qcow2",
    "34": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/34/Cloud/{arch}/images/Fedora-Cloud-Base-34-1.2.{arch}.qcow2",
    "35": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/35/Cloud/{arch}/images/Fedora-Cloud-Base-35-1.2.{arch}.qcow2",
    "36": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/36/Cloud/{arch}/images/Fedora-Cloud-Base-36-1.5.{arch}.qcow2",
    "37": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/37/Cloud/{arch}/images/Fedora-Cloud-Base-37-1.7.{arch}.qcow2",
    "38": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/38/Cloud/{arch}/images/Fedora-Cloud-Base-38-1.6.{arch}.qcow2",
    "39": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/39/Cloud/{arch}/images/Fedora-Cloud-Base-39-1.5.{arch}.qcow2",
    "40": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/40/Cloud/{arch}/images/Fedora-Cloud-Base-Generic.{arch}-40-1.14.qcow2",
    "41": "https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/41/Cloud/{arch}/images/Fedora-Cloud-Base-Generic-41-1.4.{arch}.qcow2",

    "42": "https://fedora.mirror.garr.it/fedora/linux/releases/42/Cloud/{arch}/images/Fedora-Cloud-Base-Generic-42-1.1.{arch}.qcow2",
    "43": "https://fedora.mirror.garr.it/fedora/linux/releases/43/Cloud/{arch}/images/Fedora-Cloud-Base-Generic-43-1.6.{arch}.qcow2",
    "44": "https://fedora.mirror.garr.it/fedora/linux/releases/44/Cloud/{arch}/images/Fedora-Cloud-Base-Generic-44-1.7.{arch}.qcow2"
}

CLOUD_IMAGE_URLS = {
    # Ubuntu
    "ubuntu": "https://cloud-images.ubuntu.com/{version}/current/{version}-server-cloudimg-{arch}.img",
    
    # Debian
    "debian": "https://cdimage.debian.org/cdimage/cloud/{version}/latest/debian-{version}-genericcloud-{arch}.qcow2",
    
    # Fedora
    "fedora": "https://fedora.mirror.garr.it/fedora/linux/releases/{version}/Cloud/{arch}/images/Fedora-Cloud-Base-Generic-{version}.{arch}.qcow2",
    
    # CentOS Stream
    "centos": "https://cloud.centos.org/centos/{version}/{arch}/images/CentOS-Stream-{version}-GenericCloud.qcow2",
    
    # openSUSE Leap
    "opensuse": "https://download.opensuse.org/repositories/Cloud:/Images/openSUSE_Leap_{version}/jeos/openSUSE-Leap-{version}-JeOS.{arch}-Current.qcow2"
}