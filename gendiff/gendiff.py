import gendiff.formatters as formatters
from gendiff.parser import parse_file


def create_node(status, value, new_value=None):
    return {'status': status, 'value': value, 'new_value': new_value}


def create_diff_tree(first_dict, second_dict): # noqa flake8(C901)
    if not isinstance(first_dict, dict) or not isinstance(second_dict, dict):
        return first_dict or second_dict

    keys = first_dict.keys() | second_dict.keys()
    diff = {}
    for key in keys:
        value1 = first_dict.get(key)
        value2 = second_dict.get(key)
        if key not in second_dict:
            value = create_diff_tree(value1, value1)
            diff[key] = create_node(formatters.DELETED, value)
        elif key not in first_dict:
            value = create_diff_tree(value2, value2)
            diff[key] = create_node(formatters.ADDED, value)
        elif isinstance(value1, dict) and isinstance(value2, dict):
            value = create_diff_tree(value1, value2)
            diff[key] = create_node(formatters.UNCHANGED, value)
        elif value1 == value2:
            diff[key] = create_node(formatters.UNCHANGED, value1)
        else:
            value1 = create_diff_tree(value1, value1)
            value2 = create_diff_tree(value2, value2)
            diff[key] = create_node(formatters.CHANGED, value1, value2)
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    json1 = parse_file(file_path1)
    json2 = parse_file(file_path2)

    if format_name == 'stylish':
        formatter = formatters.stylish
    else:
        formatter = formatters.plain

    diff = create_diff_tree(json1, json2)
    return formatter(diff)
