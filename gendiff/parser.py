import json
import os

import yaml


def read_json(file_path):
    with open(file_path) as f:
        result = json.load(f)
    return result


def read_yaml(file_path):
    with open(file_path) as f:
        result = yaml.full_load(f)
    return result


def get_parser(file_path):
    _, extension = os.path.splitext(file_path)
    if extension in (".yaml", ".yml"):
        return read_yaml
    return read_json


def parse_file(file_path):
    parse = get_parser(file_path)
    return parse(file_path)
