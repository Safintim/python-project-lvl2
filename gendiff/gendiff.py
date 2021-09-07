from gendiff import formatters
from gendiff.parser import parse_file


DELETED = 'deleted'
ADDED = 'added'
CHANGED = 'changed'
UNCHANGED = 'unchanged'


def create_node(status, value, new_value=None):
    return {'status': status, 'value': value, 'new_value': new_value}


def get_dict_diff(first_dict, second_dict): # noqa flake8(C901)
    if not isinstance(first_dict, dict) or not isinstance(second_dict, dict):
        return first_dict or second_dict

    keys = first_dict.keys() | second_dict.keys()
    diff = {}
    for key in keys:
        value1 = first_dict.get(key)
        value2 = second_dict.get(key)
        if key not in second_dict:
            value = get_dict_diff(value1, value1)
            diff[key] = create_node(formatters.DELETED, value)
        elif key not in first_dict:
            value = get_dict_diff(value2, value2)
            diff[key] = create_node(formatters.ADDED, value)
        elif isinstance(value1, dict) and isinstance(value2, dict):
            value = get_dict_diff(value1, value2)
            diff[key] = create_node(formatters.UNCHANGED, value)
        elif value1 == value2:
            diff[key] = create_node(formatters.UNCHANGED, value1)
        else:
            value1 = get_dict_diff(value1, value1)
            value2 = get_dict_diff(value2, value2)
            diff[key] = create_node(formatters.CHANGED, value1, value2)
    return diff


def generate_diff(file_path1, file_path2, formatter=formatters.stylish):
    json1 = parse_file(file_path1)
    json2 = parse_file(file_path2)

    diff = get_dict_diff(json1, json2)
    return formatter(diff)
