import ipaddress
import psutil

from .parser import get
from ..core import colors

def get_provider_networks(config):

    networks_list = get(config, "neutron.provider_networks", [])
    result = []

    for net in networks_list:
        net_info = {
            "bridge": net.get("bridge"),
            "name": net.get("name"),
            "type": net.get("type")
        }
        result.append(net_info)

    return result

def interface_exists(if_name: str) -> bool:
    return if_name in psutil.net_if_addrs()

def validate_ip(value: str, field_name: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        print(f"{colors.RED}Error: '{field_name}' contains an invalid IP: {value}{colors.RESET}")
        return False

def validate_cidr(value: str, field_name: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        print(f"{colors.RED}Error: '{field_name}' contains an invalid network CIDR: {value}{colors.RESET}")
        return False

# --- Passwords ---
def validate_passwords(config) -> bool:
    ok = True
    required = ["ADMIN_PASSWORD", "SERVICE_PASSWORD", "RABBITMQ_PASSWORD", "DATABASE_PASSWORD", "DEMO_PASSWORD"]
    for key in required:
        value = get(config, f"passwords.{key}")
        if not value:
            print(f"{colors.RED}Error: passwords.{key} is not set{colors.RESET}")
            ok = False
    return ok

# --- Public network ---

def validate_host_network(config) -> bool:

    ok = True

    host_network_fields = [
        "network.HOST_IP",
        "network.HOST_IP_NETMASK",
    ]

    cidr_fields = ["network.HOST_IP_CIDR"]

    for field in cidr_fields:
        value = get(config, field)
        if not value:
            ok = False
            print(f"{colors.RED}Error: Field '{field}' is missing.{colors.RESET}")
        elif not validate_cidr(value, field):
            ok = False
            print(f"{colors.RED}Error: Field '{field}' has invalid CIDR: {value}{colors.RESET}")

    # Validate IP fields
    for field in host_network_fields:
        value = get(config, field)
        if not value:
            ok = False
            print(f"{colors.RED}Error: Field '{field}' is missing.{colors.RESET}")
        elif not validate_ip(value, field):
            ok = False

    return ok


def validate_public_network(config) -> bool:

    ok = True

    ip_fields = [
        "public_network.PUBLIC_SUBNET_GATEWAY",
        "public_network.PUBLIC_SUBNET_RANGE_START",
        "public_network.PUBLIC_SUBNET_RANGE_END",
    ]
    cidr_fields = ["public_network.PUBLIC_SUBNET_CIDR"]

    # Validate CIDR fields
    for field in cidr_fields:
        value = get(config, field)
        if not value:
            ok = False
            print(f"{colors.RED}Error: Field '{field}' is missing.{colors.RESET}")
        elif not validate_cidr(value, field):
            ok = False
            print(f"{colors.RED}Error: Field '{field}' has invalid CIDR: {value}{colors.RESET}")

    # Validate IP fields
    for field in ip_fields:
        value = get(config, field)
        if not value:
            ok = False
            print(f"{colors.RED}Error: Field '{field}' is missing.{colors.RESET}")
        elif not validate_ip(value, field):
            ok = False
            print(f"{colors.RED}Error: Field '{field}' has invalid IP: {value}{colors.RESET}")

    # Validate DNS servers
    dns_servers = get(config, "public_network.PUBLIC_SUBNET_DNS_SERVERS", [])
    for i, dns in enumerate(dns_servers):
        if not validate_ip(dns, f"public_network.PUBLIC_SUBNET_DNS_SERVERS[{i}]"):
            ok = False
            print(f"{colors.RED}Error: DNS server at index {i} is invalid: {dns}{colors.RESET}")

    return ok

# --- Neutron ---
def validate_neutron(config) -> bool:
    ok = True
    driver = get(config, "neutron.DRIVER")
    if driver not in ("ovs", "ovn"):
        print(f"{colors.RED}Error: neutron.DRIVER must be 'ovs' or 'ovn' (got '{driver}'){colors.RESET}")
        ok = False

    if driver == "ovs":
        ovs_fields = [
            "neutron.ovs.PUBLIC_BRIDGE",
            "neutron.ovs.INTERNAL_BRIDGE",
            "neutron.ovs.PUBLIC_BRIDGE_INTERFACE",
        ]
        for field in ovs_fields:
            value = get(config, field)
            if not value:
                print(f"{colors.RED}Error: '{field}' is not set{colors.RESET}")
                ok = False

    if driver == "ovn":
        ovn_fields = [
            "neutron.ovn.OVN_PUBLIC_BRIDGE",
            "neutron.ovn.OVN_PUBLIC_BRIDGE_INTERFACE",
            "neutron.ovn.OVN_NB_PORT",
            "neutron.ovn.OVN_SB_PORT",
        ]
        for field in ovn_fields:
            value = get(config, field)
            if not value:
                print(f"{colors.RED}Error: '{field}' is not set{colors.RESET}")
                ok = False

    # Tenant network
    neutron_driver = get(config, "neutron.DRIVER")
    tenant_type = get(config, "neutron.tenant_network.TYPE")
    vni_range = get(config, "neutron.tenant_network.VNI_RANGE")

    networks = get_provider_networks(config)

    ovs_create_bridges = get(config, "neutron.ovs.CREATE_BRIDGES")

    public_bridge_interface_ovs = get(config, "neutron.ovs.PUBLIC_BRIDGE_INTERFACE")

    if ovs_create_bridges not in ("yes", "no"):
            print(f"{colors.RED}Error: '{ovs_create_bridges}' must be 'yes' or 'no' (got '{value}'){colors.RESET}")
            ok = False

    if not interface_exists(public_bridge_interface_ovs):
        print(f"{colors.RED}The interface '{public_bridge_interface_ovs}' specified in neutron.ovs.PUBLIC_BRIDGE_INTERFACE does not exist.{colors.RESET}")
        ok = False

    for net in networks:
        net_type = net["type"]
        if net_type not in ["geneve", "flat"]:
            print(f"{colors.RED}Error: Invalid network type '{net_type}' specified in field {net}{colors.RESET}")
            ok = False

    if tenant_type not in ["geneve", "flat"]:
        print(f"{colors.RED}Error: Invalid network type '{tenant_type}' specified in field neutron.tenant_network.TYPE{colors.RESET}")
        ok = False

    if not tenant_type and not vni_range and neutron_driver == "ovn":
        print(f"{colors.RED}Error: neutron.tenant_network.TYPE or VNI_RANGE not set{colors.RESET}")
        ok = False
    elif not tenant_type and neutron_driver == "ovs":
        print(f"{colors.RED}Error: neutron.tenant_network.TYPE not set{colors.RESET}")
        ok = False

    # Provider networks
    provider_networks = get(config, "neutron.provider_networks", [])
    if not provider_networks:
        print(f"{colors.RED}Error: neutron.provider_networks is empty{colors.RESET}")
        ok = False
    else:
        for i, net in enumerate(provider_networks):
            if not net.get("name") or not net.get("bridge") or not net.get("type"):
                print(f"{colors.RED}Error: neutron.provider_networks[{i}] missing required keys{colors.RESET}")
                ok = False

    return ok

# --- Cinder ---
def validate_cinder(config) -> bool:
    ok = True
    cinder_fields = [
        "cinder.lvm.CINDER_VOLUME_LVM_IMAGE_FILE_PATH",
        "cinder.lvm.CINDER_VOLUME_LVM_IMAGE_SIZE_IN_GB",
    ]
    for field in cinder_fields:
        value = get(config, field)
        if not value:
            print(f"{colors.RED}Error: '{field}' is not set{colors.RESET}")
            ok = False
    return ok

# --- Compute ---
def validate_compute(config) -> bool:
    ok = True
    compute_fields = [
        "compute.NOVA_COMPUTE_VIRT_TYPE",
        "compute.CPU_ALLOCATION_RATIO",
        "compute.RAM_ALLOCATION_RATIO",
        "compute.DISK_ALLOCATION_RATIO",
    ]
    for field in compute_fields:
        value = get(config, field)
        if value is None:
            print(f"{colors.RED}Error: '{field}' is not set{colors.RESET}")
            ok = False
    return ok

# --- Optional services ---
def validate_optional_services(config) -> bool:
    ok = True

    services = [
        "optional_services.INSTALL_CINDER",
        "optional_services.INSTALL_HORIZON",
    ]

    for field in services:
        value = get(config, field)
        if value not in ("yes", "no"):
            print(f"{colors.RED}Error: '{field}' must be 'yes' or 'no' (got '{value}'){colors.RESET}")
            ok = False
    return ok

# --- OpenStack ---
def validate_openstack(config) -> bool:
    ok = True
    fields = ["openstack.OPENSTACK_RELEASE", "openstack.REGION_NAME"]
    for field in fields:
        value = get(config, field)
        if not value:
            print(f"{colors.RED}Error: '{field}' is not set{colors.RESET}")
            ok = False
    return ok

def validate_all(config) -> bool:
    ok = True
    ok &= validate_passwords(config)
    ok &= validate_host_network(config)
    ok &= validate_public_network(config)
    ok &= validate_neutron(config)
    ok &= validate_cinder(config)
    ok &= validate_compute(config)
    ok &= validate_optional_services(config)
    ok &= validate_openstack(config)
    return ok