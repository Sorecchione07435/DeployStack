from ..utils.run_command_utils import run_command
from ..utils.apt_utils import apt_install, apt_update
from ..utils.config_parser import parse_config, get, resolve_vars
from ..utils import colors

import os

config_file_path = "/etc/mysql/mariadb.conf.d/99-openstack.cnf"

def install_pkgs():
    
    packages = ["mariadb-server", "python3-pymysql"]

    success =  apt_install(packages, ux_text=f"Installing MariaDB packages...")

    if not success:
            print(f"Installation of packages failed. Aborting installation.")
            return False
    return True

def conf_mariadb(config):

    ip_address = get(config, "network.HOST_IP", None)

    if not os.path.isfile(config_file_path):

        with open(config_file_path, "w") as f:
            f.write(f"""[mysqld]
    bind-address = {ip_address}

    default-storage-engine = innodb
    innodb_file_per_table = on
    max_connections = 4096
    collation-server = utf8_general_ci
    character-set-server = utf8
    """)

def finalize():
     
    message = f"Restarting MySQL..."
    restart_cmd = ["systemctl", "restart", "mysql"]

    result = run_command(restart_cmd, message)

    if not result:
            return False
    return True

def create_services_databases(config):
    db_password = get(config, "passwords.DATABASE_PASSWORD")
    ip_address = get(config, "network.HOST_IP")

    install_cinder = get(config, "cinder.INSTALL_CINDER", "no") == "yes"

    databases = ["keystone", "glance", "placement", "nova_api", "nova_cell0", "nova", "neutron"]
    if install_cinder:
        databases.append("cinder")

    sql_commands = []

    for db in databases:
        sql_commands.append(f"CREATE DATABASE IF NOT EXISTS {db};")

    users = {
        "keystone": ["keystone"],
        "glance": ["glance"],
        "placement": ["placement"],
        "nova_api": ["nova"],
        "nova_cell0": ["nova"],
        "nova": ["nova"],
        "neutron": ["neutron"]
    }
    if install_cinder:
        users["cinder"] = ["cinder"]

    for db, usernames in users.items():
        for user in usernames:
            for host in ["localhost", "%", ip_address]:
                sql_commands.append(
                    f"CREATE USER IF NOT EXISTS '{user}'@'{host}' IDENTIFIED BY '{db_password}';"
                )
                sql_commands.append(
                    f"GRANT ALL PRIVILEGES ON {db}.* TO '{user}'@'{host}';"
                )

    sql_commands.append("FLUSH PRIVILEGES;")

    sql_string = " ".join(sql_commands)

    result = run_command(["mysql", "-u", "root", "-e", sql_string], "Creating services databases...")

    if not result:
        return False
    
    return True

def run_setup_mariadb(config):

    if not install_pkgs():
        print(f"\n{colors.RED}MariaDB installation failed. Aborting.{colors.RESET}")
        return False
    
    conf_mariadb(config)
    
    if not finalize():
        return False
    
    if not create_services_databases(config):
        return False

    print(f"\n{colors.YELLOW}MariaDB and Databases configured successfully!{colors.RESET}\n")
    return True