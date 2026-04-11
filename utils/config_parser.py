import yaml
import re
import os

def resolve_vars(config):
    pattern = re.compile(r"\$(\w+)")

    for key, value in config.items():
        match = pattern.match(value)
        if match:
            ref_key = match.group(1)
            config[key] = config.get(ref_key, value)

    return config

def parse_config(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' does not exist.")

    with open(file_path, "r") as f:
        config = yaml.safe_load(f) or {}

    return config


def get(config_dict, key, default=None, required=False):
    keys = key.split(".")
    value = config_dict

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            if required:
                raise KeyError(f"Required configuration key '{key}' not found.")
            return default

    return value

def to_bool(value):

    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ["yes", "true", "1"]